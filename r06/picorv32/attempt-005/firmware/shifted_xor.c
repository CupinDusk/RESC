typedef unsigned int u32;
__attribute__((noinline)) u32 workload(volatile const u32 *in){u32 h=0x9e3779b9u; for(u32 i=0;i<8;i++) h=(h<<5)^(h>>2)^in[i]; return h;}
int main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}
