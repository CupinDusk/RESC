#include <array>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <stdexcept>
#include <cstdint>
#include <vector>
using S=std::array<int64_t,19>;
// Independent contract model. Inputs are the current edge's first five fields;
// outputs are derived only from the preceding outputs and those current inputs.
S next_state(S before,const S &inputs) {
 S n=before; for(int i=0;i<5;i++)n[i]=inputs[i]; n[18]=0;
 auto reject=[&](int reason){n[7]=n[8]=n[9]=0;n[10]=reason;};
 if(inputs[0]) {for(int i=5;i<19;i++)n[i]=0;n[13]=1000;return n;}
 if(inputs[1]) {
   if(before[7]) {reject(5);n[5]=n[6]=0;}
   else {n[5]=1;n[6]=n[8]=n[9]=n[10]=0;n[11]=inputs[3];n[12]=inputs[4];n[14]=n[15]=n[16]=n[17]=0;}
 } else if(before[7]) {
   if(inputs[4]!=before[12])reject(4);
   else if(inputs[2])reject(8);
   else if(uint64_t(before[17])==UINT64_MAX || uint64_t(before[16])==UINT32_MAX)reject(7);
   else {
     n[17]++; bool pulse=before[15]+1==before[12];
     n[15]=pulse?0:before[15]+1;
     if(pulse) {n[16]++;n[14]--;n[18]=1;if(n[14]==0){n[7]=0;n[8]=1;}}
   }
 } else if(inputs[2]) {
   n[5]=n[8]=n[9]=0;
   int why=0;
   if(!before[5])why=1;
   else if(before[6]!=2 || inputs[4]!=before[12])why=2;
   else if(!before[11] || !before[12])why=6;
   else if(200*uint64_t(inputs[4])>201*uint64_t(before[13]) || 200*uint64_t(before[13])>201*uint64_t(inputs[4]))why=3;
   n[10]=why;
   if(!why){n[7]=n[9]=1;n[13]=before[12];n[14]=before[11];n[15]=n[16]=n[17]=0;}
 } else if(before[5]) {
   n[6]=inputs[4]!=before[12]?0:std::min<int64_t>(2,before[6]+1);
 }
 return n;
}
#ifndef MODEL_ONLY
std::vector<int64_t> parse(const std::string&line){std::vector<int64_t>v;std::istringstream s(line);std::string f;while(std::getline(s,f,','))v.push_back(std::stoll(f));return v;}
int main(int argc,char**argv){try{
 if(argc!=3)return 2;std::string dir=argv[1];std::ifstream sc(dir+"/SCENARIOS.csv"),rle(dir+"/TICKS_RLE.csv");
 if(!sc||!rle)throw std::runtime_error("trace absent");
 std::array<S,44> state{};std::array<uint64_t,44>edges{},starts{},finishes{},pulses{};std::string line;
 std::getline(sc,line);int ns=0;while(std::getline(sc,line)){auto v=parse(line);if(v.size()!=22||v[0]!=ns||v[1]!=(ns>=32)||v[2]!=(ns>=32?ns-32:ns))throw std::runtime_error("scenario framing");for(int j=0;j<19;j++)state[ns][j]=v[j+3];ns++;}if(ns!=44)throw std::runtime_error("scenario count");
 std::getline(rle,line);uint64_t all=0,rows=0,active=0;int last=-1;while(std::getline(rle,line)){
  auto v=parse(line);if(v.size()!=22)throw std::runtime_error("row width");int id=v[0];if(id<0||id>=44||id<last||v[1]!=edges[id]+1||v[2]<=0)throw std::runtime_error("trace framing");last=id;rows++;
  for(int64_t k=0;k<v[2];k++){
   S actual=state[id];for(int j=0;j<19;j++)actual[j]+=v[j+3];auto expected=next_state(state[id],actual);
   for(int j=0;j<19;j++)if(actual[j]!=expected[j])throw std::runtime_error("transition mismatch scenario="+std::to_string(id)+" edge="+std::to_string(edges[id]+1)+" field="+std::to_string(j)+" observed="+std::to_string(actual[j])+" expected="+std::to_string(expected[j]));
   for(int j=0;j<19;j++)if(actual[j]<0)throw std::runtime_error("negative state");
   if(!state[id][7]&&actual[7])starts[id]++;
   if(!state[id][8]&&actual[8])finishes[id]++;
   pulses[id]+=actual[18];if(id<32&&state[id][7])active++;
   state[id]=actual;edges[id]++;all++;
  }
 }
 uint64_t vp=0;for(int id=0;id<44;id++){if(!edges[id])throw std::runtime_error("empty scenario");if(id<32){if(starts[id]!=6||finishes[id]!=6)throw std::runtime_error("job event population");vp+=pulses[id];}else if(state[id][9]||state[id][7]||state[id][8]||state[id][10]<1||state[id][10]>4)throw std::runtime_error("invalid final state");}
 std::ofstream o(argv[2]);o<<"{\"status\":\"PASS\",\"decoded_edges\":"<<all<<",\"rle_rows\":"<<rows<<",\"valid_active_edges\":"<<active<<",\"valid_pulses\":"<<vp<<",\"scenario_edges\":[";for(int id=0;id<44;id++){if(id)o<<',';o<<edges[id];}o<<"]}\n";std::cout<<"PASS every decoded edge: "<<all<<"\n";return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
#endif
