typedef unsigned int u32;
__attribute__((noinline)) u32 workload(volatile const u32 *in){u32 s=0; for(u32 i=0;i<8;i++) s+=in[i]; return s;}
int main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}
