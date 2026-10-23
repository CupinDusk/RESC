// Sufficient exactness recognizer, independent of family/expect metadata.
// Include after frozen_jobs.hpp, which supplies the unmodified R05 functions.
bool adjacent_exact(const Plan&p){
 const int n=p.n;
 if(n<1||p.pos.size()!=size_t(n)||p.R.size()!=size_t(n)*size_t(n))return false;
 if(p.pos.front()<=0)return false;
 for(int i=1;i<n;i++)if(p.pos[i-1]>=p.pos[i])return false;
 std::vector<int> rank(n,0),order(n,-1);
 for(int i=0;i<n;i++){
  if(p.R[i*n+i])return false;
  for(int j=i+1;j<n;j++){
   auto a=p.R[i*n+j],b=p.R[j*n+i];
   if(a>1||b>1||int(a)+int(b)!=1)return false;
   rank[j]+=a;rank[i]+=b;
  }
 }
 for(int i=0;i<n;i++){
  if(rank[i]<0||rank[i]>=n||order[rank[i]]!=-1)return false;
  order[rank[i]]=i;
 }
 // Validate the whole supplied matrix, rather than assuming transitive closure.
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)
  if(p.R[i*n+j]!=uint8_t(rank[i]<rank[j]))return false;
 for(int i=0;i<n;){
  if(order[i]==i){i++;continue;}
  if(i+1>=n||order[i]!=i+1||order[i+1]!=i)return false;
  i+=2;
 }
 return true;
}
struct SpecializedPlan{Plan p;bool adj=false,quartet_called=false;};
SpecializedPlan prepare_specialized(const Plan&seed,int route){
 require(route==4||route==5,"specialized route");
 SpecializedPlan result;result.p=prepare_plan(seed,2);
 if(!result.p.cheap)result.adj=adjacent_exact(result.p);
 result.p.exact=result.p.cheap||result.adj;
 if(route==5&&!result.p.exact){result.quartet_called=true;result.p.exact=quartet(result.p);}
 return result;
}
uint64_t complete_job_all(const Plan&seed,int route,int count,Scratch&scratch){
 if(route<=3)return complete_job(seed,route,count,scratch);
 auto prepared=prepare_specialized(seed,route);const auto&p=prepared.p;
 uint64_t h=1469598103934665603ULL;
 for(int qi=0;qi<count;qi++){
  auto[ri,d]=seed.queries[qi%48];
  bool result=query(p,seed.rect[ri],d,3,scratch);
  h=(h^uint64_t(result+2*ri+131*d))*1099511628211ULL;
 }
 return h;
}
