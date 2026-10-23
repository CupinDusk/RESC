// Six complete routes, using frozen R05 algorithms through a separate wrapper.
#include "frozen_jobs.hpp"
#include "specialized.hpp"
struct SixBatch{int block,sid,q;std::array<int,6> routes;};
int main(int argc,char**argv){
 require(argc==2,"mode validate|time required");bool timing=std::string(argv[1])=="time";
 require(timing||std::string(argv[1])=="validate","invalid mode");
 if(timing){std::ifstream gate("ROOT_TIMING_GATE.json");require(bool(gate),"root timing gate missing");}
 std::ifstream in("inputs.txt");require(bool(in),"inputs missing");int np,ns;in>>np>>ns;
 std::vector<Plan>plans(np);
 for(auto&p:plans){
  int ne;in>>p.id>>p.sid>>p.n>>ne>>p.expect;p.pos.resize(p.n);for(auto&x:p.pos)in>>x;
  for(int e=0;e<ne;e++){int a,b;in>>a>>b;p.edges.push_back({a,b});}
  for(auto&r:p.rect){r.l.resize(p.n);r.u.resize(p.n);for(auto&x:r.l)in>>x;for(auto&x:r.u)in>>x;}
  for(int k=0;k<48;k++){int ri,d;in>>ri>>d;p.queries.push_back({ri,d});}
 }
 std::vector<Stratum>strata(ns);
 for(auto&s:strata){int ni;in>>s.id>>s.reps>>ni;s.ids.resize(ni);for(auto&x:s.ids)in>>x;}
 require(bool(in)&&np==15&&ns==15,"input parse/count failure");
 std::ifstream sf("schedule.txt");int nr;sf>>nr;std::vector<SixBatch>schedule(nr);
 for(auto&b:schedule){sf>>b.block>>b.sid>>b.q;for(auto&x:b.routes)sf>>x;}
 require(bool(sf)&&nr==9*15*4,"schedule parse failure");Scratch scratch;
 if(!timing){
  std::ofstream out("validation.csv");out<<"plan,rectangle,delta,decision,raw_floyd,closure_floyd,cheap,quartet,specialized,specialized_quartet\n";
  std::ofstream census("routing_census.csv");census<<"plan,n,route,cheap_flag,adj_flag,exact_flag,quartet_called,queries,graph,beta_reject,cheap_exact,span,other_exact\n";
  uint64_t checked=0;
  for(auto&seed:plans){
   Plan raw=prepare_plan(seed,0),closed=prepare_plan(seed,1),cheap=prepare_plan(seed,2),quad=prepare_plan(seed,3);
   auto sp=prepare_specialized(seed,4),sq=prepare_specialized(seed,5);
   for(auto[ri,d]:seed.queries){
    auto&r=seed.rect[ri];bool a=bf(raw,r,d,scratch,true),b=bf(closed,r,d,scratch,true);
    bool c=floyd(raw,r,d,scratch),e=floyd(closed,r,d,scratch);
    bool f=query(cheap,r,d,2,scratch),g=query(quad,r,d,3,scratch);
    bool h=query(sp.p,r,d,3,scratch),j=query(sq.p,r,d,3,scratch);
    require(a==b&&a==c&&a==e&&a==f&&a==g&&a==h&&a==j,"raw/closure/Floyd/routed mismatch");
    out<<seed.id<<','<<ri<<','<<d<<','<<a<<','<<c<<','<<e<<','<<f<<','<<g<<','<<h<<','<<j<<'\n';checked++;
   }
   for(int route=0;route<6;route++){
    Plan p;bool adj=false,qcalled=false;
    if(route<4){p=prepare_plan(seed,route);qcalled=route==3&&!p.cheap;}
    else {auto s=prepare_specialized(seed,route);p=std::move(s.p);adj=s.adj;qcalled=s.quartet_called;}
    std::array<int,5>paths{};
    for(auto[ri,d]:seed.queries){int path;query(p,seed.rect[ri],d,route<2?0:route<4?route:3,scratch,&path);paths[path]++;}
    census<<seed.id<<','<<seed.n<<','<<route<<','<<p.cheap<<','<<adj<<','<<p.exact<<','<<qcalled<<",48";
    for(int x:paths)census<<','<<x;census<<'\n';
   }
  }
  std::ofstream expected("expected_batches.csv");expected<<"stratum,queries,expected_checksum\n";
  for(auto&s:strata)for(int q:{1,48,192,768}){
   uint64_t sums[6]={};
   for(int route=0;route<6;route++)for(int id:s.ids)sums[route]+=complete_job_all(plans[id],route,q,scratch);
   for(int route=1;route<6;route++)require(sums[0]==sums[route],"complete-job hash mismatch");
   expected<<s.id<<','<<q<<','<<sums[0]<<'\n';
  }
  std::cout<<"PASS_VALIDATION distinct_queries="<<checked<<" six_routes complete_batch_hashes=60\n";return 0;
 }
 std::ifstream ef("expected_batches.csv");require(bool(ef),"validated expected hashes missing");
 std::string line;std::getline(ef,line);std::vector<std::array<uint64_t,4>>expected(ns);
 while(std::getline(ef,line)){for(auto&ch:line)if(ch==',')ch=' ';std::istringstream row(line);int sid,q;uint64_t h;row>>sid>>q>>h;require(bool(row),"expected parse");expected[sid][q==1?0:q==48?1:q==192?2:3]=h;}
 for(auto&s:strata)for(int q:{1,48,192,768})for(int route=0;route<6;route++){
  uint64_t h=0;for(int id:s.ids)h+=complete_job_all(plans[id],route,q,scratch);
  require(h==expected[s.id][q==1?0:q==48?1:q==192?2:3],"warmup expected mismatch");checksum+=h;
 }
 std::ofstream out("complete_times.csv");out<<"block,stratum,queries,position,route,repeats,jobs_per_repeat,elapsed_ns,checksum,expected_checksum\n";
 for(auto&b:schedule){auto&s=strata[b.sid];
  for(int position=0;position<6;position++){
   int route=b.routes[position];uint64_t h=0;auto start=Clock::now();
   for(int rep=0;rep<s.reps;rep++)for(int id:s.ids){
    asm volatile("" : : "g"(&plans[id]) : "memory");h+=complete_job_all(plans[id],route,b.q,scratch);
   }
   auto stop=Clock::now();uint64_t want=expected[s.id][b.q==1?0:b.q==48?1:b.q==192?2:3]*uint64_t(s.reps);
   require(h==want,"timed expected mismatch");checksum+=h;
   auto elapsed=std::chrono::duration_cast<std::chrono::nanoseconds>(stop-start).count();
   out<<b.block<<','<<s.id<<','<<b.q<<','<<position<<','<<route<<','<<s.reps<<','<<s.ids.size()<<','<<elapsed<<','<<h<<','<<want<<'\n';
  }
  out.flush();if(b.sid==0)std::cout<<"complete block="<<b.block<<" census Q="<<b.q<<std::endl;
 }
 std::cout<<"PASS_TIMING checksum="<<checksum<<" steady="<<Clock::is_steady<<" timer_period="<<Clock::period::num<<'/'<<Clock::period::den<<" sizeof_signed128="<<sizeof(I)<<std::endl;
}
