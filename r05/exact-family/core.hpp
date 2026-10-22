// Exact synthetic audit microbenchmark. No GPU/physical claims.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <string>
#include <utility>
#include <vector>
using I=__int128_t;using Clock=std::chrono::steady_clock;
volatile uint64_t checksum=0;
struct Rect{std::vector<int64_t> l,u;};
struct Plan{int id,sid,n,expect;std::vector<int64_t> pos;std::vector<std::pair<int,int>> edges,pairs;std::vector<uint8_t> R;std::array<Rect,48> rect;std::vector<std::pair<int,int>> queries,survivors;bool cheap=false,exact=false;int64_t span=0;};
struct Stratum{int id,reps;std::vector<int> ids;};
struct Schedule{int block,sid;std::array<int,4> routes;std::array<int,3> prep;};
[[noreturn]]void fail(const std::string&s){std::cerr<<s<<"\n";std::exit(2);}void require(bool b,const std::string&s){if(!b)fail(s);}
void close(Plan&p){int n=p.n;p.R.assign(n*n,0);for(auto [a,b]:p.edges)p.R[a*n+b]=1;for(int k=0;k<n;k++)for(int i=0;i<n;i++)if(p.R[i*n+k])for(int j=0;j<n;j++)p.R[i*n+j]|=p.R[k*n+j];p.pairs.clear();for(int i=0;i<n;i++){require(!p.R[i*n+i],"cyclic ranking");for(int j=0;j<n;j++)if(p.R[i*n+j])p.pairs.push_back({i,j});}p.span=p.pos.back()-p.pos.front()+1;}
bool cheap_flag(const Plan&p){bool up=true,down=true;int source=-1,target=-1;bool common_source=true,common_target=true;for(auto[a,b]:p.pairs){up&=p.pos[a]<p.pos[b];down&=p.pos[a]>p.pos[b];if(source<0)source=a;else common_source&=source==a;if(target<0)target=b;else common_target&=target==b;}return p.n<4||up||down||common_source||common_target;}
bool quartet(const Plan&p){int n=p.n;auto ok=[&](int a,int b,int c,int d){auto x=std::llabs(p.pos[a]-p.pos[c])+std::llabs(p.pos[b]-p.pos[d]);auto y=std::llabs(p.pos[a]-p.pos[d])+std::llabs(p.pos[b]-p.pos[c]);bool u=p.R[a*n+c]&&p.R[b*n+d],v=p.R[a*n+d]&&p.R[b*n+c];return !((u||v)&&std::min(u?x:INT64_MAX,v?y:INT64_MAX)>std::min(x,y));};for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++){if(!ok(a,b,c,d)||!ok(a,c,b,d)||!ok(a,d,b,c)||!ok(b,c,a,d)||!ok(b,d,a,c)||!ok(c,d,a,b))return false;}return true;}
struct Scratch{std::vector<I>w,h,floyd;std::vector<int>pred;};
void graph(const Plan&p,const Rect&r,int delta,Scratch&s){int n=p.n;s.w.resize(n*n);for(int a=0;a<n;a++)for(int b=0;b<n;b++){I w=a==b?0:I(r.u[b])-r.l[a]+I(delta)*std::llabs(p.pos[a]-p.pos[b]);if(!p.R.empty()&&p.R[b*n+a]&&w>0)w=0;s.w[a*n+b]=w;}if(p.R.empty())for(auto[a,b]:p.edges)s.w[b*n+a]=std::min<I>(s.w[b*n+a],0);}
bool bf(const Plan&p,const Rect&r,int delta,Scratch&s,bool certificate){int n=p.n;graph(p,r,delta,s);s.h.assign(n,0);s.pred.assign(n,-1);int changed=-1;for(int turn=0;turn<n;turn++){changed=-1;for(int a=0;a<n;a++)for(int b=0;b<n;b++)if(s.h[b]>s.h[a]+s.w[a*n+b]){s.h[b]=s.h[a]+s.w[a*n+b];s.pred[b]=a;changed=b;}if(changed<0){if(certificate)for(int a=0;a<n;a++)for(int b=0;b<n;b++)require(s.h[b]<=s.h[a]+s.w[a*n+b],"bad feasible potential");return true;}}if(certificate){int v=changed;for(int i=0;i<n;i++){require(v>=0,"missing pred");v=s.pred[v];}int start=v,count=0;I weight=0;do{int prev=s.pred[v];require(prev>=0,"missing cycle pred");weight+=s.w[prev*n+v];v=prev;require(++count<=n,"bad cycle extraction");}while(v!=start);require(weight<0,"nonnegative reject certificate");}return false;}
bool floyd(const Plan&p,const Rect&r,int delta,Scratch&s){int n=p.n;graph(p,r,delta,s);s.floyd=s.w;for(int k=0;k<n;k++){for(int i=0;i<n;i++)for(int j=0;j<n;j++){I v=s.floyd[i*n+k]+s.floyd[k*n+j];if(v<s.floyd[i*n+j])s.floyd[i*n+j]=v;}for(int i=0;i<n;i++)if(s.floyd[i*n+i]<0)return false;}return true;}
// route codes: 0direct;1beta;2cheap+span;3quartet union+span.
// output path: 0graph,1beta reject,2cheap exact,3span,4quartet-only exact.
bool query(const Plan&p,const Rect&r,int delta,int route,Scratch&s,int*path=nullptr){if(path)*path=0;if(route){bool beta_reject=false,span_admit=true;bool exact_route=route>=2&&(p.cheap||(route==3&&p.exact));bool need_span=route>=2&&(!exact_route||path);I cap=std::max<int64_t>(1,p.span-2);for(auto[a,b]:p.pairs){I deficit=I(r.l[a])-r.u[b];I allowed=I(delta)*std::llabs(p.pos[a]-p.pos[b]);if(deficit>allowed){beta_reject=true;break;}if(need_span&&cap*deficit>allowed)span_admit=false;}if(beta_reject){if(path)*path=1;return false;}if(exact_route&&!path)return true;if(route>=2){if(p.cheap){if(path)*path=2;return true;}if(span_admit){if(path)*path=3;return true;}if(route==3&&p.exact){if(path)*path=4;return true;}}}return bf(p,r,delta,s,false);}
