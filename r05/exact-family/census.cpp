// Untimed actual routing census, separate from the frozen one-time measurements.
#include "core.hpp"
int main(){
 std::ifstream in("inputs.txt");int np,ns;in>>np>>ns;require(np==15&&ns==15,"count");
 std::ofstream out("routing_census.csv");out<<"plan,n,cheap_flag,quartet_flag,queries,cheap_graph,quartet_graph\n";
 for(int z=0;z<np;z++){
  Plan p;int ne;in>>p.id>>p.sid>>p.n>>ne>>p.expect;p.pos.resize(p.n);for(auto&v:p.pos)in>>v;
  for(int k=0;k<ne;k++){int a,b;in>>a>>b;p.edges.push_back({a,b});}
  for(auto&r:p.rect){r.l.resize(p.n);r.u.resize(p.n);for(auto&v:r.l)in>>v;for(auto&v:r.u)in>>v;}
  for(int k=0;k<48;k++){int i,d;in>>i>>d;p.queries.push_back({i,d});}
  require(bool(in),"parse");close(p);p.cheap=cheap_flag(p);p.exact=p.cheap||quartet(p);
  Scratch s;int cg=0,qg=0;
  for(auto[i,d]:p.queries){int a,b;require(query(p,p.rect[i],d,2,s,&a)&&query(p,p.rect[i],d,3,s,&b),"false planted result");cg+=a==0;qg+=b==0;}
  out<<p.id<<','<<p.n<<','<<p.cheap<<','<<p.exact<<",48,"<<cg<<','<<qg<<'\n';
 }
}
