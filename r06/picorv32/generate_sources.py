"""Generate the fixed protocol population; does not inspect any run result."""
from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    proto=json.loads((HERE/'PROTOCOL.json').read_text(encoding='utf-8'))
    assert sha(HERE/'upstream/picorv32.v')==proto['upstream']['picorv32.v_sha256']
    out=HERE/'firmware';out.mkdir(exist_ok=False)
    bodies={
      'array_sum':'u32 s=0; for(u32 i=0;i<8;i++) s+=in[i]; return s;',
      'shifted_xor':'u32 h=0x9e3779b9u; for(u32 i=0;i<8;i++) h=(h<<5)^(h>>2)^in[i]; return h;',
      'xorshift':'u32 x=in[0]; if(!x)x=1; for(u32 i=0;i<24;i++){x^=x<<13; x^=x>>17; x^=x<<5;} return x;',
      'crc32':'u32 c=0xffffffffu; for(u32 i=0;i<8;i++){c^=in[i]&255u; for(u32 j=0;j<8;j++)c=(c>>1)^((0u-(c&1u))&0xedb88320u);} return ~c;',
      'popcount':'u32 s=0; for(u32 i=0;i<8;i++){u32 x=in[i]; while(x){s++; x&=x-1u;}} return s;',
      'subtractive_gcd':'u32 a=(in[0]&1023u)+1u,b=(in[1]&1023u)+1u; while(a!=b){if(a>b)a-=b; else b-=a;} return a;'
    }
    for name,body in bodies.items():
        (out/(name+'.c')).write_text('typedef unsigned int u32;\n__attribute__((noinline)) u32 workload(volatile const u32 *in){'+body+'}\nint main(void){u32 r=workload((volatile const u32 *)0x8000u); *(volatile u32 *)0x10000000u=r; return 0;}\n',encoding='utf-8')
    (out/'startup.S').write_text('.section .text.start,"ax"\n.global _start\n_start:\n.option push\n.option norelax\nla gp, __global_pointer$\n.option pop\nli sp, 0xff00\ncall main\nebreak\n1: j 1b\n',encoding='utf-8')
    (out/'link.ld').write_text('ENTRY(_start)\nSECTIONS { . = 0; .text : { *(.text.start) *(.text*) } .rodata : { *(.rodata*) } .data : { *(.data*) *(.sdata*) } PROVIDE(__global_pointer$ = . + 0x800); .bss : { *(.bss*) *(.sbss*) *(COMMON) } /DISCARD/ : { *(.comment) *(.riscv.attributes) *(.eh_frame*) } }\n',encoding='utf-8')
    jobs=[];reports=[]
    for fn in bodies:
      for inp in range(2):
       for gi,g in enumerate(proto['guards']):
        for pn,path in g['paths'].items():
         rid=len(reports);reports.append(dict(report=rid,function=fn,input=inp,guard=gi,path=pn))
         for slot,flag in enumerate(proto['flags']):jobs.append(dict(job=len(jobs),report=rid,slot=slot,function=fn,input=inp,flag=flag,D=path[slot],guard_num=g['numerator'],guard_den=g['denominator']))
    (HERE/'JOBS_CONFIG.json').write_text(json.dumps(dict(reports=reports,jobs=jobs),indent=2)+'\n',encoding='utf-8')
    with (HERE/'jobs.txt').open('w',encoding='utf-8') as f:
      f.write(str(len(jobs))+'\n')
      for j in jobs:f.write(' '.join(str(j[k]) for k in ['job','report','slot','function','input','flag','D','guard_num','guard_den'])+'\n')
    # Only the already checked graph core and rigorous log helper are reused.
    source=HERE.parents[1]/'r05-analysis/hopper-reference-rtl'
    provenance={}
    for n in ['audit_core.py','exact_logs.py']:
      shutil.copyfile(source/n,HERE/n);provenance[n]={'source':'r05-analysis/hopper-reference-rtl/'+n,'sha256':sha(HERE/n)}
    (HERE/'CORE_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    (HERE/'PROSPECTIVE_BINDING.json').write_text(json.dumps({'protocol_sha256':sha(HERE/'PROTOCOL.json'),'upstream_binding_sha256':sha(HERE/'UPSTREAM_BINDING.json'),'generation':'Fixed protocol population, no DUT/cost read','inputs':proto['inputs'],'firmware_sources':{p.name:sha(p) for p in out.iterdir()}},indent=2)+'\n',encoding='utf-8')
    print('Generated fixed 36 binaries / 72 function-input-flag combinations / 576 jobs / 96 reports')
if __name__=='__main__':main()
