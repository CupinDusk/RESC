// Complete per-ranking Boolean-auditor jobs; no GPU or certificate-service timing.
#include <sstream>
#include "core.hpp"
struct Batch{int block,sid,q;std::array<int,4> routes;};
Plan prepare_plan(const Plan&source,int route){
 Plan p;p.id=source.id;p.sid=source.sid;p.n=source.n;p.pos=source.pos;p.edges=source.edges;
 if(route>=1)close(p);
 if(route>=2)p.cheap=cheap_flag(p);
 if(route==3)p.exact=p.cheap||quartet(p);
 return p;
}
uint64_t complete_job(const Plan&seed,int route,int count,Scratch&scratch){
 Plan p=prepare_plan(seed,route);uint64_t h=1469598103934665603ULL;
 for(int qi=0;qi<count;qi++){
  auto[ri,d]=seed.queries[qi%48];
  bool result=query(p,seed.rect[ri],d,route<2?0:route,scratch);
  h=(h^uint64_t(result+2*ri+131*d))*1099511628211ULL;
 }
 return h;
}
