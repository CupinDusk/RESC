// Author-side independent verification only. Never measures execution time.
// No include or code generation from the submitted core/benchmark.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <utility>
#include <vector>
using Wide=__int128_t;
struct Edge {int from,to; Wide weight;};
struct Plan {
 int id,sid,n,flag; std::vector<long long> x;
 std::vector<std::pair<int,int>> rank,queries;
 std::array<std::vector<long long>,8> lower,upper;
};
void demand(bool value,const char* message) {if(!value)throw std::runtime_error(message);}
std::vector<std::vector<bool>> reachability(const Plan& p) {
 std::vector<std::vector<int>> next(p.n);
 for(auto e:p.rank)next[e.first].push_back(e.second);
 std::vector<std::vector<bool>> reachable(p.n,std::vector<bool>(p.n));
 for(int source=0;source<p.n;++source) {
  std::vector<int> pending=next[source];
  while(!pending.empty()) {
   int current=pending.back(); pending.pop_back();
   if(reachable[source][current])continue;
   reachable[source][current]=true;
   for(int v:next[current])pending.push_back(v);
  }
  demand(!reachable[source][source],"independent ranking cycle");
 }
 return reachable;
}
long long distance(const Plan& p,int a,int b) {return std::max(p.x[a],p.x[b])-std::min(p.x[a],p.x[b]);}
std::vector<Edge> constraints(const Plan& p,int rectangle,int budget,bool closed,const std::vector<std::vector<bool>>& reach) {
 std::vector<Edge> edges;
 // Store every inequality separately, including ranking edges; do not merge
 // ranking edges with the dense data matrix as the benchmark does.
 for(int target=0;target<p.n;++target)for(int source=0;source<p.n;++source)
  edges.push_back({source,target,Wide(p.upper[rectangle][target])-p.lower[rectangle][source]+Wide(budget)*distance(p,source,target)});
 if(closed) {
  for(int winner=0;winner<p.n;++winner)for(int loser=0;loser<p.n;++loser)
   if(reach[winner][loser])edges.push_back({loser,winner,0});
 } else for(auto [winner,loser]:p.rank)edges.push_back({loser,winner,0});
 return edges;
}
bool floyd_check(int n,const std::vector<Edge>& edges) {
 const Wide infinity=Wide(1)<<100;
 std::vector<Wide> dist(n*n,infinity);
 for(int i=0;i<n;++i)dist[i*n+i]=0;
 for(auto e:edges)dist[e.from*n+e.to]=std::min(dist[e.from*n+e.to],e.weight);
 for(int middle=0;middle<n;++middle) {
  // Same mathematical Floyd algorithm, independently written on a separately
  // constructed multigraph; negative diagonal checks avoid negative-cycle growth.
  for(int target=0;target<n;++target)for(int source=0;source<n;++source)
   dist[source*n+target]=std::min(dist[source*n+target],dist[source*n+middle]+dist[middle*n+target]);
  for(int i=0;i<n;++i)if(dist[i*n+i]<0)return false;
 }
 return true;
}
bool certificate_check(int n,const std::vector<Edge>& edges) {
 std::vector<Wide> labels(n); std::vector<int> predecessor(n,-1);
 int changed=-1;
 for(int pass=0;pass<n;++pass) {
  changed=-1;
  // Reverse explicit-edge order differs from the original dense BF scan.
  for(int index=int(edges.size())-1;index>=0;--index) {
   auto e=edges[index];
   if(labels[e.to]>labels[e.from]+e.weight) {
    labels[e.to]=labels[e.from]+e.weight;predecessor[e.to]=index;changed=e.to;
   }
  }
  if(changed<0) {
   for(auto e:edges)demand(labels[e.to]<=labels[e.from]+e.weight,"independent invalid potential");
   return true;
  }
 }
 int node=changed;
 for(int step=0;step<n;++step) {demand(predecessor[node]>=0,"independent missing cycle predecessor");node=edges[predecessor[node]].from;}
 int start=node,length=0; Wide weight=0;
 do {
  demand(predecessor[node]>=0,"independent missing cycle edge");
  auto e=edges[predecessor[node]];demand(e.to==node,"independent wrong cycle direction");
  weight+=e.weight;node=e.from;demand(++length<=n,"independent nonclosing cycle");
 }while(node!=start);
 demand(weight<0,"independent nonnegative negative-cycle certificate");
 return false;
}
bool quartet_check(const Plan& p,const std::vector<std::vector<bool>>& reach) {
 // Enumerate unordered source pairs and unordered disjoint target pairs;
 // inspect both possible bijections. No call to the submitted classifier.
 for(int a=0;a<p.n;++a)for(int b=a+1;b<p.n;++b)
  for(int c=0;c<p.n;++c)if(c!=a&&c!=b)
   for(int d=c+1;d<p.n;++d)if(d!=a&&d!=b) {
    long long one=distance(p,a,c)+distance(p,b,d),two=distance(p,a,d)+distance(p,b,c);
    bool permitted_one=reach[a][c]&&reach[b][d],permitted_two=reach[a][d]&&reach[b][c];
    if(!permitted_one&&!permitted_two)continue;
    long long minimum=std::min(one,two);
    if(!(permitted_one&&one==minimum)&&!(permitted_two&&two==minimum))return false;
   }
 return true;
}
int main() {
 try {
  std::ifstream input("inputs.txt");int count,strata;input>>count>>strata;
  demand(count==870&&strata==51,"independent input counts");
  std::ofstream output("independent_graph.csv");output<<"plan,rectangle,delta,raw_floyd,closed_floyd,raw_bf_certificate,closed_bf_certificate\n";
  long long checked=0,feasible=0,exact_flags=0;
  for(int index=0;index<count;++index) {
   Plan p;int edge_count;input>>p.id>>p.sid>>p.n>>edge_count>>p.flag;p.x.resize(p.n);
   demand(p.id==index,"independent input ID");for(auto& x:p.x)input>>x;
   for(int k=1;k<p.n;++k)demand(p.x[k]>p.x[k-1],"independent unsorted positions");
   for(int k=0;k<edge_count;++k){int a,b;input>>a>>b;p.rank.push_back({a,b});}
   for(int r=0;r<8;++r){p.lower[r].resize(p.n);p.upper[r].resize(p.n);for(auto& x:p.lower[r])input>>x;for(auto& x:p.upper[r])input>>x;for(int k=0;k<p.n;++k)demand(p.lower[r][k]<=p.upper[r][k],"independent invalid interval");}
   for(int k=0;k<48;++k){int rectangle,budget;input>>rectangle>>budget;p.queries.push_back({rectangle,budget});}
   auto reach=reachability(p);bool exact=quartet_check(p,reach);demand(exact==bool(p.flag),"independent quartet flag mismatch");exact_flags+=exact;
   for(auto [rectangle,budget]:p.queries) {
    auto raw=constraints(p,rectangle,budget,false,reach),closed=constraints(p,rectangle,budget,true,reach);
    bool a=floyd_check(p.n,raw),b=floyd_check(p.n,closed),c=certificate_check(p.n,raw),d=certificate_check(p.n,closed);
    demand(a==b&&a==c&&a==d,"independent feasibility mismatch");
    output<<p.id<<','<<rectangle<<','<<budget<<','<<a<<','<<b<<','<<c<<','<<d<<'\n';++checked;feasible+=a;
   }
  }
  demand(bool(input),"independent parse failure");
  std::cout<<"PASS_INDEPENDENT_GRAPH queries="<<checked<<" feasible="<<feasible<<" quartet_exact_plans="<<exact_flags<<" raw_closed_Floyd_and_edge_certificates=4_per_query\n";
 } catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 2;}
}
