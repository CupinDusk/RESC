#include "netlist.cpp"
#define MODEL_ONLY
#include "edge_oracle.cpp"
using Dut=cxxrtl_design::p_reference__job;
#define GET(x) int64_t(d.p_##x.get<uint64_t>())
#define SET(x,v) d.p_##x.set<uint32_t>(uint32_t(v))
S sample(Dut&d){return {GET(rst),GET(commandreset),GET(start),GET(cfgn),GET(cfgd),GET(licensed),GET(settled),GET(busy),GET(done),GET(valid),GET(reason),GET(nlatched),GET(heldd),GET(previousd),GET(remaining),GET(phase),GET(pulses),GET(timer),GET(jobpulse)};}
struct Bench{
 Dut d;S prev{};int edges=0;
 Bench(){SET(clk,0);SET(rst,0);SET(commandreset,0);SET(start,0);SET(cfgn,0);SET(cfgd,0);d.step();prev=sample(d);}
 void edge(int r,int c,int s,int n,int div){
  S in=prev;in[0]=r;in[1]=c;in[2]=s;in[3]=n;in[4]=div;
  S exp=next_state(prev,in);SET(rst,r);SET(commandreset,c);SET(start,s);SET(cfgn,n);SET(cfgd,div);
  SET(clk,0);d.step();SET(clk,1);d.step();SET(clk,0);d.step();S actual=sample(d);edges++;
  if(actual!=exp){for(int j=5;j<19;j++)if(actual[j]!=exp[j]){std::cerr<<"detected edge="<<edges<<" field="<<j<<" actual="<<actual[j]<<" expected="<<exp[j]<<'\n';break;}throw std::runtime_error("RTL semantic mismatch");}prev=actual;
 }
 void reset(){edge(1,0,0,0,0);}
 void arm(int n,int div,int quiet=2){edge(0,1,0,n,div);for(int k=0;k<quiet;k++)edge(0,0,0,n,div);}
 void start(int n,int div){edge(0,0,1,n,div);}
};
int main(){try{
 // Every test compares each post-edge output, so a mutant is killed by a
 // contract-observable transition and not by a textual/synthesis difference.
 {Bench b;b.reset();b.arm(3,1000);b.start(3,1000);for(int i=0;i<3001;i++)b.edge(0,0,0,780,1000);}
 {Bench b;b.reset();b.start(3,1000);}
 {Bench b;b.reset();b.arm(3,1000,1);b.start(3,1000);}
 {Bench b;b.reset();b.arm(3,1006);b.start(3,1006);}
 {Bench b;b.reset();b.arm(3,1005);b.start(3,1005);b.edge(0,0,0,780,1005);b.edge(0,0,0,780,1006);}
 {Bench b;b.reset();b.arm(0,1000);b.start(0,1000);}
 {Bench b;b.reset();b.arm(3,0);b.start(3,0);}
 {Bench b;b.reset();b.arm(3,1000);b.start(3,1000);b.edge(0,1,0,3,1000);}
 {Bench b;b.reset();b.arm(3,1000);b.start(3,1000);b.start(3,1000);}
 std::cout<<"PASS independent synthesized RTL harness\n";return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
