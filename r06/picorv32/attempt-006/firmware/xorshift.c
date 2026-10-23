typedef unsigned int u32;
__attribute__((noinline)) u32 workload(volatile const u32 *in){u32 x=in[0]; if(!x)x=1; for(u32 i=0;i<24;i++){x^=x<<13; x^=x>>17; x^=x<<5;} return x;}
int main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}
