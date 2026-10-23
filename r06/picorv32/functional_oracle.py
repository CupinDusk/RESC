"""Independent RV32I functional interpreter and algorithm-level Python oracle.

This checks firmware semantics; it is never the DUT or a cycle-count source.
"""
from pathlib import Path
import argparse,hashlib,json,math,struct,zlib
MASK=(1<<32)-1
def sx(x,b):return (x^(1<<(b-1)))-(1<<(b-1))
def functional(name,a):
 if name=='array_sum':return sum(a)&MASK
 if name=='shifted_xor':
  h=0x9e3779b9
  for x in a:h=((h<<5)^(h>>2)^x)&MASK
  return h
 if name=='xorshift':
  x=a[0] or 1
  for _ in range(24):
   x^=(x<<13)&MASK;x^=x>>17;x^=(x<<5)&MASK
  return x
 if name=='crc32':return zlib.crc32(bytes(x&255 for x in a))
 if name=='popcount':return sum(x.bit_count() for x in a)
 if name=='subtractive_gcd':return math.gcd((a[0]&1023)+1,(a[1]&1023)+1)
 raise ValueError(name)
def execute(data,inputs):
 mem=bytearray(data);assert len(mem)==65536
 for i,x in enumerate(inputs):struct.pack_into('<I',mem,32768+4*i,x)
 regs=[0]*32;pc=0;result=[];count=0;digest=hashlib.sha256()
 def load(a,n,sign=False):
  assert a% n==0 and 0<=a<=65536-n
  x=int.from_bytes(mem[a:a+n],'little');return sx(x,n*8)&MASK if sign else x
 while count<200000:
  assert pc%4==0 and pc<8192
  ins=load(pc,4);digest.update(struct.pack('<II',pc,ins));count+=1
  op=ins&127;rd=(ins>>7)&31;f3=(ins>>12)&7;r1=(ins>>15)&31;r2=(ins>>20)&31;f7=ins>>25;a=regs[r1];b=regs[r2];dest=None;npc=(pc+4)&MASK
  if ins==0x00100073:
   assert pc==24 and len(result)==1
   return dict(result=result[0],halt_pc=pc,instructions=count,instruction_stream_sha256=digest.hexdigest(),only_rv32i=True)
  if op==0x37:dest=ins&0xfffff000
  elif op==0x17:dest=pc+(ins&0xfffff000)
  elif op==0x6f:
   imm=((ins>>31)<<20)|(((ins>>12)&255)<<12)|(((ins>>20)&1)<<11)|(((ins>>21)&1023)<<1);dest=pc+4;npc=(pc+sx(imm,21))&MASK
  elif op==0x67:
   assert f3==0;dest=pc+4;npc=(a+sx(ins>>20,12))&MASK&~1
  elif op==0x63:
   imm=((ins>>31)<<12)|(((ins>>7)&1)<<11)|(((ins>>25)&63)<<5)|(((ins>>8)&15)<<1)
   take={0:a==b,1:a!=b,4:sx(a,32)<sx(b,32),5:sx(a,32)>=sx(b,32),6:a<b,7:a>=b}[f3]
   if take:npc=(pc+sx(imm,13))&MASK
  elif op==3:
   addr=(a+sx(ins>>20,12))&MASK;n={0:1,1:2,2:4,4:1,5:2}[f3];dest=load(addr,n,f3<2)
  elif op==0x23:
   imm=((ins>>25)<<5)|((ins>>7)&31);addr=(a+sx(imm,12))&MASK;n={0:1,1:2,2:4}[f3]
   if addr==0x10000000:assert n==4;result.append(b)
   else:
    assert 8192<=addr<=65536-n and not (32768<=addr<32800) and addr%n==0
    mem[addr:addr+n]=(b&((1<<(n*8))-1)).to_bytes(n,'little')
  elif op==0x13:
   im=sx(ins>>20,12)
   if f3==0:dest=a+im
   elif f3==2:dest=int(sx(a,32)<im)
   elif f3==3:dest=int(a<(im&MASK))
   elif f3==4:dest=a^(im&MASK)
   elif f3==6:dest=a|(im&MASK)
   elif f3==7:dest=a&(im&MASK)
   elif f3==1:assert f7==0;dest=a<<r2
   elif f3==5:assert f7 in [0,32];dest=(sx(a,32) if f7==32 else a)>>r2
   else:raise AssertionError('bad opimm')
  elif op==0x33:
   assert f7 in [0,32] and (f7==0 or f3 in [0,5])
   if f3==0:dest=a-b if f7==32 else a+b
   elif f3==1:dest=a<<(b&31)
   elif f3==2:dest=int(sx(a,32)<sx(b,32))
   elif f3==3:dest=int(a<b)
   elif f3==4:dest=a^b
   elif f3==5:dest=(sx(a,32) if f7==32 else a)>>(b&31)
   elif f3==6:dest=a|b
   elif f3==7:dest=a&b
  elif op==0x0f:assert f3==0
  else:raise AssertionError(f'unsupported RV32I opcode {ins:08x} pc{pc}')
  if dest is not None and rd:regs[rd]=dest&MASK
  regs[0]=0;pc=npc
 raise AssertionError('ISA instruction timeout')
def main():
 p=argparse.ArgumentParser();p.add_argument('--attempt',type=Path,required=True);a=p.parse_args();proto=json.loads((a.attempt/'PROTOCOL.json').read_text(encoding='utf-8'));rows=[]
 for fn in proto['functions']:
  for flag in proto['flags']:
   path=a.attempt/'images'/(fn+'_'+flag+'.ram')
   for ii,inp in enumerate(proto['inputs']):
    r=execute(path.read_bytes(),inp);expect=functional(fn,inp);assert r['result']==expect
    rows.append(dict(function=fn,flag=flag,input=ii,expected=expect,ram_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**r))
 (a.attempt/'FUNCTIONAL_ORACLE.json').write_text(json.dumps(dict(status='PASS_72_INDEPENDENT_ISA_AND_ALGORITHM_RESULTS_NOT_DUT_CYCLES',rows=rows),indent=2)+'\n',encoding='utf-8');print('PASS 72 independent RV32I instruction executions and algorithm checks')
if __name__=='__main__':main()
