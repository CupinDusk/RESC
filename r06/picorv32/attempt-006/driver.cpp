// Actual processor and reference-controller CXXRTL, synchronous host memory.
#define cxxrtl_design_create picorv32_design_create
#include "core.cpp"
#undef cxxrtl_design_create
#define cxxrtl_design_create controller_design_create
#include "controller.cpp"
#undef cxxrtl_design_create
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "sha256.hpp"
using Core=cxxrtl_design::p_core__wrapper;
using Ctrl=cxxrtl_design::p_controller;
#define G(d,x) uint64_t((d).p_##x.get<uint64_t>())
#define S(d,x,v) (d).p_##x.template set<uint64_t>(uint64_t(v))
static std::string context;
void req(bool v,const std::string&s){if(!v)throw std::runtime_error(context+": "+s);}
template<class D>void edge(D&d){S(d,clk,0);d.step();S(d,clk,1);d.step();S(d,clk,0);d.step();}
using State=std::array<int64_t,18>;
State sample(Ctrl&d){return {int64_t(G(d,rst)),int64_t(G(d,commandreset)),int64_t(G(d,start)),int64_t(G(d,stop)),int64_t(G(d,cfgd)),int64_t(G(d,licensed)),int64_t(G(d,settled)),int64_t(G(d,busy)),int64_t(G(d,valid)),int64_t(G(d,reason)),int64_t(G(d,heldd)),int64_t(G(d,previousd)),int64_t(G(d,phase)),int64_t(G(d,pulses)),int64_t(G(d,timer)),int64_t(G(d,pulse)),int64_t(G(d,gnum)),int64_t(G(d,gden))};}
const char*fields="rst,commandreset,start,stop,cfgd,licensed,settled,busy,valid,reason,heldd,previousd,phase,pulses,timer,pulse,gnum,gden";
struct Trace {
 std::ofstream &out,&hashes;int scenario;State prev{},delta{};uint64_t edgecount=0,first=0,count=0;Sha256 hash;
 Trace(std::ofstream&o,std::ofstream&h,int s,const State&i):out(o),hashes(h),scenario(s),prev(i){}
 void flush(){if(!count)return;out<<scenario<<','<<first<<','<<count;for(auto x:delta)out<<','<<x;out<<'\n';count=0;}
 void append(const State&s){State v;for(int i=0;i<18;i++)v[i]=s[i]-prev[i];++edgecount;if(count&&v==delta)++count;else{flush();delta=v;first=edgecount;count=1;}prev=s;
  // Expanded canonical record: timerLE64,phaseLE32,pulsesLE32,pulse,busy,valid,reason.
  hash.le(s[14],8);hash.le(s[12],4);hash.le(s[13],4);hash.le(s[15],1);hash.le(s[7],1);hash.le(s[8],1);hash.le(s[9],1);
 }
 ~Trace(){flush();hashes<<scenario<<','<<edgecount<<','<<edgecount*20<<','<<hash.end()<<'\n';}
};
void tick(Ctrl&d,Trace&t){edge(d);t.append(sample(d));}
void zero(Ctrl&d){S(d,clk,0);S(d,rst,0);S(d,commandreset,0);S(d,start,0);S(d,stop,0);S(d,cfgd,1000);S(d,gnum,201);S(d,gden,200);d.step();}
void reset(Ctrl&d,Trace&t){S(d,rst,1);tick(d,t);S(d,rst,0);}
void command(Ctrl&d,Trace&t,uint32_t div,int q){S(d,cfgd,div);S(d,commandreset,1);tick(d,t);S(d,commandreset,0);for(int i=0;i<q;i++)tick(d,t);}
void start(Ctrl&d,Trace&t){S(d,start,1);tick(d,t);S(d,start,0);}
void checked(Ctrl&d,Trace&t){auto old=sample(d);req(old[7]&&old[8]&&!old[9],"controller valid pre-edge");tick(d,t);auto s=sample(d);bool p=old[12]+1==old[10];req(s[14]==old[14]+1&&s[12]==(p?0:old[12]+1)&&s[13]==old[13]+p&&s[15]==p,"actual reference timer/divider transition");req(s[7]&&s[8]&&!s[9]&&s[10]==old[10],"held divider/source status");}
struct Machine {
 Core c;std::vector<uint8_t>ram;uint64_t cycles=0,writes=0;uint32_t result=0,lastfetch=0,lastinsn=0;bool ebreak=false;std::ofstream&trace;int job;
 Machine(const std::string&path,int input,int j,std::ofstream&t):ram(65536),trace(t),job(j){
  std::ifstream f(path,std::ios::binary);f.read((char*)ram.data(),ram.size());req(f.gcount()==65536,"RAM research image size");
  static const uint32_t in[2][8]={{1,7,19,31,85,170,255,305419896},{3735928559u,0,4294967295u,17,256,65535,2147483648u,42}};
  for(int i=0;i<8;i++)for(int b=0;b<4;b++)ram[32768+4*i+b]=uint8_t(in[input][i]>>(b*8));
  S(c,clk,0);S(c,resetn,0);S(c,mem__ready,0);S(c,mem__rdata,0);c.step();for(int i=0;i<8;i++)edge(c);S(c,resetn,1);c.step();req(!G(c,trap),"reset trap");
 }
 void step(){
  S(c,clk,0);c.step();uint32_t v=G(c,mem__valid),a=G(c,mem__addr),w=G(c,mem__wdata),s=G(c,mem__wstrb),ins=G(c,mem__instr),r=0;
  if(v){req((a&3)==0,"unaligned native word bus");if(a==0x10000000){req(s==15&&!ins,"result MMIO fullword write only");result=w;writes++;}else{req(a<65536-3,"unmapped bus address");for(int b=0;b<4;b++)r|=uint32_t(ram[a+b])<<(8*b);
   if(s){req(a>=8192&&!(a>=32768&&a<32800)&&!ins,"RAM write violates firmware/input contract");for(int b=0;b<4;b++)if(s&(1<<b))ram[a+b]=uint8_t(w>>(8*b));}
   if(ins){req(!s&&a<8192,"instruction fetch outside firmware");lastfetch=a;lastinsn=r;if(r==0x00100073)ebreak=true;}
  }}
  S(c,mem__ready,v);S(c,mem__rdata,r);c.step();S(c,clk,1);c.step();S(c,clk,0);c.step();++cycles;
  trace<<job<<','<<cycles<<','<<v<<','<<ins<<','<<a<<','<<w<<','<<s<<','<<r<<','<<G(c,trap)<<','<<G(c,trace__valid)<<','<<G(c,trace__data)<<','<<lastfetch<<','<<lastinsn<<'\n';
 }
};
struct Job{int id,report,slot,input,div,num,den;std::string fn,flag;};
int main(int argc,char**argv){if(argc!=3)return 2;std::string inp=argv[1],out=argv[2];try{
 Sha256 test;test.add("abc",3);req(test.end()=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","SHA256 known answer");
 std::ifstream f(inp+"/jobs.txt");int nj;f>>nj;req(nj==576,"fixed job population");std::vector<Job>js;for(int z=0;z<nj;z++){Job j;f>>j.id>>j.report>>j.slot>>j.fn>>j.input>>j.flag>>j.div>>j.num>>j.den;req(bool(f)&&j.id==z,"job parse");js.push_back(j);}
 std::ofstream rle(out+"/REFERENCE_RLE.csv"),sc(out+"/SCENARIOS.csv"),hs(out+"/REFERENCE_EXPANDED_HASHES.csv"),ct(out+"/CORE_CYCLES.csv"),jobs(out+"/JOBS.csv"),bad(out+"/INVALID_CONTROLS.csv");
 rle<<"scenario,first_edge,count,"<<fields<<'\n';sc<<"scenario,"<<fields<<'\n';hs<<"scenario,edges,expanded_bytes,sha256\n";ct<<"job,core_cycle,pre_mem_valid,pre_mem_instr,pre_mem_addr,pre_mem_wdata,pre_mem_wstrb,pre_mem_rdata,post_trap,post_trace_valid,post_trace_data,lastfetch,lastinsn\n";
 jobs<<"job,report,slot,function,input,flag,D,previous_D,N,T,result,result_writes,ebreak_fetched,lastfetch,lastinsn,controller_valid,reason,source_valid,ref_start,ref_trap,ref_stop\n";
 bad<<"id,expected_reason,actual_reason,valid,busy,graph_audit_licensed\n";
 uint64_t allrefs=0,allcores=0;int done=0;
 for(int report=0;report<96;report++){
  Ctrl d;zero(d);S(d,gnum,js[6*report].num);S(d,gden,js[6*report].den);d.step();auto init=sample(d);sc<<report;for(auto x:init)sc<<','<<x;sc<<'\n';Trace tr(rle,hs,report,init);reset(d,tr);
  for(int slot=0;slot<6;slot++){
   auto j=js[6*report+slot];context="job "+std::to_string(j.id);Machine m(inp+"/images/"+j.fn+"_"+j.flag+".ram",j.input,j.id,ct);auto prev=G(d,previousd);command(d,tr,j.div,2);start(d,tr);req(G(d,busy)&&G(d,valid)&&!G(d,reason),"licensed start");auto startref=tr.edgecount;
   while(!G(m.c,trap)){
    checked(d,tr);if(G(d,pulse)){req(m.cycles<1000000,"declared core timeout");m.step();}
   }
   auto T=G(d,timer),N=m.cycles,trapref=tr.edgecount;req(T==N*uint64_t(j.div)&&G(d,pulses)==N&&G(d,phase)==0,"observed T equals executed core count times held divider");req(m.writes==1&&m.ebreak&&m.lastinsn==0x00100073,"common result/ebreak termination contract");
   S(d,stop,1);tick(d,tr);S(d,stop,0);req(!G(d,busy)&&G(d,valid)&&G(d,timer)==T,"stop edge excluded from timer");
   jobs<<j.id<<','<<j.report<<','<<j.slot<<','<<j.fn<<','<<j.input<<','<<j.flag<<','<<j.div<<','<<prev<<','<<N<<','<<T<<','<<m.result<<','<<m.writes<<','<<m.ebreak<<','<<m.lastfetch<<','<<m.lastinsn<<','<<G(d,valid)<<','<<G(d,reason)<<",1,"<<startref<<','<<trapref<<','<<tr.edgecount<<'\n';allcores+=N;done++;
  }
  allrefs+=tr.edgecount;std::cout<<"report "<<report<<" complete, jobs="<<done<<'\n'<<std::flush;
 }
 int reasons[8]={1,2,2,3,4,6,5,8};
 for(int id=0;id<8;id++){
  context="invalid controller "+std::to_string(id);Ctrl d;zero(d);auto init=sample(d);sc<<96+id;for(auto x:init)sc<<','<<x;sc<<'\n';Trace tr(rle,hs,96+id,init);reset(d,tr);
  if(id!=0)command(d,tr,id==3?1006:id==5?0:1000,id==1?0:id==2?1:2);start(d,tr);
  if(id==4){S(d,cfgd,1001);tick(d,tr);}if(id==6){S(d,commandreset,1);tick(d,tr);S(d,commandreset,0);}if(id==7)start(d,tr);
  req(G(d,reason)==uint64_t(reasons[id])&&!G(d,valid)&&!G(d,busy),"specific invalid control unknown");bad<<id<<','<<reasons[id]<<','<<G(d,reason)<<','<<G(d,valid)<<','<<G(d,busy)<<",0\n";allrefs+=tr.edgecount;
 }
 std::ofstream sum(out+"/RTL_RESULTS.json");sum<<"{\"status\":\"PASS_ACTUAL_PICORV32_CXXRTL_REFERENCE_DESIGN_PENDING_INDEPENDENT_GATE\",\"jobs\":"<<done<<",\"reports\":96,\"core_cycles\":"<<allcores<<",\"reference_edges\":"<<allrefs<<",\"controller_controls\":8,\"per_reference_edge_checks\":true,\"mismatches\":0}\n";
 std::cout<<"PASS "<<done<<" actual processor jobs\n";return 0;
 }catch(const std::exception&e){std::ofstream f(out+"/SIMULATION_FAILURE.txt");f<<e.what()<<'\n';std::cerr<<e.what()<<'\n';return 1;}}
