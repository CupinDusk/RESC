typedef unsigned int u32;
__attribute__((noinline)) u32 workload(volatile const u32 *in){u32 a=(in[0]&1023u)+1u,b=(in[1]&1023u)+1u; while(a!=b){if(a>b)a-=b; else b-=a;} return a;}
int main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}
