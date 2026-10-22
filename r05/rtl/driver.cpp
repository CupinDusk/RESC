// Executes the actual Yosys-generated CXXRTL. Every sample is post-reference-edge.
#include "netlist.cpp"
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Dut=cxxrtl_design::p_reference__job;
#define GET(x) uint64_t(d.p_##x.get<uint64_t>())
#define SET(x,v) d.p_##x.set<uint32_t>(uint32_t(v))
static std::string context;
void require(bool x,const std::string&s){if(!x)throw std::runtime_error(context+": "+s);}
using State=std::array<int64_t,19>;
static const char* fields="rst,commandreset,start,cfgn,cfgd,licensed,settled,busy,done,valid,reason,nlatched,heldd,previousd,remaining,phase,pulses,timer,jobpulse";
State sample(Dut&d){return {int64_t(GET(rst)),int64_t(GET(commandreset)),int64_t(GET(start)),int64_t(GET(cfgn)),int64_t(GET(cfgd)),int64_t(GET(licensed)),int64_t(GET(settled)),int64_t(GET(busy)),int64_t(GET(done)),int64_t(GET(valid)),int64_t(GET(reason)),int64_t(GET(nlatched)),int64_t(GET(heldd)),int64_t(GET(previousd)),int64_t(GET(remaining)),int64_t(GET(phase)),int64_t(GET(pulses)),int64_t(GET(timer)),int64_t(GET(jobpulse))};}
void clockedge(Dut&d){SET(clk,0);d.step();SET(clk,1);d.step();SET(clk,0);d.step();}
struct Trace {
 std::ofstream& out; int scenario; State prev{},delta{};uint64_t edge=0,first=0,count=0;
 Trace(std::ofstream&o,int s,const State&initial):out(o),scenario(s),prev(initial){}
 void flush(){if(!count)return;out<<scenario<<','<<first<<','<<count;for(auto x:delta)out<<','<<x;out<<'\n';count=0;}
 void append(const State&s){State v;for(size_t j=0;j<v.size();j++)v[j]=s[j]-prev[j];++edge;if(count&&v==delta)++count;else{flush();delta=v;first=edge;count=1;}prev=s;}
 ~Trace(){flush();}
};
void tick(Dut&d,Trace&t){clockedge(d);t.append(sample(d));}
void zero_inputs(Dut&d){SET(clk,0);SET(rst,0);SET(commandreset,0);SET(start,0);SET(cfgn,0);SET(cfgd,0);d.step();}
void scenario_row(std::ofstream&o,int sc,int type,int id,const State&s){o<<sc<<','<<type<<','<<id;for(auto x:s)o<<','<<x;o<<'\n';}
void global_reset(Dut&d,Trace&t){SET(rst,1);tick(d,t);SET(rst,0);require(GET(previousd)==1000&&!GET(licensed)&&!GET(valid)&&!GET(busy),"global reset");}
void command_reset(Dut&d,Trace&t,int n,int div,int quiet){SET(cfgn,n);SET(cfgd,div);SET(commandreset,1);tick(d,t);SET(commandreset,0);require(GET(licensed)&&GET(nlatched)==uint64_t(n)&&GET(heldd)==uint64_t(div)&&GET(settled)==0,"command reset capture");for(int k=0;k<quiet;k++)tick(d,t);}
void start(Dut&d,Trace&t){SET(start,1);tick(d,t);SET(start,0);}
void checked_busy_edge(Dut&d,Trace&t){
 auto old=sample(d);require(old[7]&&old[9]&&!old[10],"pre-edge valid busy");tick(d,t);auto s=sample(d);
 require(s[17]==old[17]+1,"timer is not incremented by one actual RTL edge");
 bool pulse=old[15]+1==old[12];
 require(s[18]==pulse,"divider pulse edge");require(s[15]==(pulse?0:old[15]+1),"divider phase");
 require(s[16]==old[16]+pulse&&s[14]==old[14]-pulse,"countdown/pulse relation");
 bool finish=pulse&&old[14]==1;require(bool(s[8])==finish&&bool(s[7])==!finish,"completion edge");
 require(s[9]&&!s[10]&&s[11]==old[11]&&s[12]==old[12],"held private count and divider");
}
struct Case{int id,vi;std::array<int,6> n,d;};
int main(int argc,char**argv){
 if(argc!=3)return 2;std::string inp=argv[1],outp=argv[2];
 try{
  std::ifstream in(inp+"/vectors.txt");require(bool(in),"vectors absent");int nc;in>>nc;require(nc==32,"valid case population");std::vector<Case> cases;
  for(int z=0;z<nc;z++){Case c;in>>c.id>>c.vi;for(int&x:c.n)in>>x;for(int&x:c.d)in>>x;require(bool(in)&&c.id==z,"case parse");cases.push_back(c);}
  std::ofstream rle(outp+"/TICKS_RLE.csv"),scs(outp+"/SCENARIOS.csv"),jobs(outp+"/JOBS.csv"),bad(outp+"/INVALID_CONTROLS.csv");
  rle<<"scenario,first_edge,count,"<<fields<<'\n';scs<<"scenario,type,id,"<<fields<<'\n';
  jobs<<"case_id,vector_id,slot,scenario,reset_edge,start_edge,completion_edge,N,D,previous_D,settled_at_start,T,lower,upper,job_pulses,valid,reason\n";
  bad<<"invalid_id,scenario,expected_reason,N,D,quiet,change_edge,changed_D,trigger_scenario_edge,actual_reason,valid,busy,done,timer,pulses,graph_audit_licensed\n";
  uint64_t all_ticks=0,valid_ticks=0,invalid_ticks=0,valid_jobs=0,all_pulses=0;
  for(const auto&c:cases){
   context="valid case "+std::to_string(c.id);Dut d;zero_inputs(d);auto init=sample(d);scenario_row(scs,c.id,0,c.id,init);Trace t(rle,c.id,init);global_reset(d,t);
   for(int j=0;j<6;j++){
    context="valid case "+std::to_string(c.id)+" slot "+std::to_string(j);int n=c.n[j],div=c.d[j];
    require(n>=1996&&n<=2100&&div>=976&&div<=1030,"predeclared width domain");
    auto before=GET(previousd);auto resetedge=t.edge+1;command_reset(d,t,n,div,2);auto settled=GET(settled);
    auto startedge=t.edge+1;start(d,t);require(GET(busy)&&GET(valid)&&!GET(reason)&&!GET(licensed),"valid start rejected");
    require(!GET(timer)&&!GET(phase)&&!GET(pulses)&&GET(remaining)==uint64_t(n),"start initialization");
    // Change the external private-count input once after capture: the RTL must
    // use its latched count. The abstraction never discloses either input.
    SET(cfgn,n+777);
    uint64_t watchdog=0;while(GET(busy)){require(++watchdog<=2200000,"bounded completion watchdog");checked_busy_edge(d,t);}
    auto T=GET(timer);require(GET(done)&&GET(valid)&&!GET(reason)&&GET(pulses)==uint64_t(n)&&!GET(remaining),"valid terminal state");
    require(T==uint64_t(n)*uint64_t(div)&&t.edge-startedge==T,"post-execution fixed-cycle induction check");
    jobs<<c.id<<','<<c.vi<<','<<j<<','<<c.id<<','<<resetedge<<','<<startedge<<','<<t.edge<<','<<n<<','<<div<<','<<before<<','<<settled<<','<<T<<','<<T-1<<','<<T+1<<','<<GET(pulses)<<','<<GET(valid)<<','<<GET(reason)<<'\n';
    valid_jobs++;valid_ticks+=T;all_pulses+=GET(pulses);
   }
   all_ticks+=t.edge;
  }
  int ni;in>>ni;require(ni==12,"invalid population");
  for(int z=0;z<ni;z++){
   int id,reason,n,div,quiet,change,changed;in>>id>>reason>>n>>div>>quiet>>change>>changed;require(bool(in)&&id==z,"invalid parse");
   int sc=32+id;context="invalid control "+std::to_string(id);Dut d;zero_inputs(d);auto init=sample(d);scenario_row(scs,sc,1,id,init);Trace t(rle,sc,init);global_reset(d,t);
   if(reason==1){SET(cfgn,n);SET(cfgd,div);for(int k=0;k<quiet;k++)tick(d,t);}else command_reset(d,t,n,div,quiet);
   start(d,t);uint64_t trigger=t.edge;
   if(reason==4){require(GET(busy)&&GET(valid),"mid-change control failed valid prefix");for(int k=1;k<change;k++)checked_busy_edge(d,t);SET(cfgd,changed);tick(d,t);trigger=t.edge;}
   require(GET(reason)==uint64_t(reason)&&!GET(valid)&&!GET(busy)&&!GET(done),"specific contract-unknown reason");
   bad<<id<<','<<sc<<','<<reason<<','<<n<<','<<div<<','<<quiet<<','<<change<<','<<changed<<','<<trigger<<','<<GET(reason)<<','<<GET(valid)<<','<<GET(busy)<<','<<GET(done)<<','<<GET(timer)<<','<<GET(pulses)<<",0\n";
   all_ticks+=t.edge;invalid_ticks+=t.edge;
  }
  require(valid_jobs==192,"all 192 jobs retained");
  std::ofstream summary(outp+"/RTL_RESULTS.json");summary<<"{\n  \"status\":\"PASS_EXECUTED_GENERATED_REFERENCE_RTL\",\n  \"valid_reports\":32,\n  \"valid_jobs\":"<<valid_jobs<<",\n  \"invalid_attempts\":12,\n  \"all_reference_edges\":"<<all_ticks<<",\n  \"valid_active_reference_edges\":"<<valid_ticks<<",\n  \"invalid_scenario_reference_edges\":"<<invalid_ticks<<",\n  \"valid_job_pulses\":"<<all_pulses<<",\n  \"per_edge_checks\":true,\n  \"mismatches\":0\n}\n";
  std::cout<<"PASS actual generated CXXRTL: "<<valid_jobs<<" jobs; "<<all_ticks<<" sampled reference edges; 12 contract-unknown controls\n";return 0;
 }catch(const std::exception&e){std::ofstream f(outp+"/SIMULATION_FAILURE.txt");f<<e.what()<<'\n';std::cerr<<e.what()<<'\n';return 1;}
}
