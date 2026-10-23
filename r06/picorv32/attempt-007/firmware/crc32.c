typedef unsigned int u32;
__attribute__((noinline)) u32 workload(volatile const u32 *in){u32 c=0xffffffffu; for(u32 i=0;i<8;i++){c^=in[i]&255u; for(u32 j=0;j<8;j++)c=(c>>1)^((0u-(c&1u))&0xedb88320u);} return ~c;}
int main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}
