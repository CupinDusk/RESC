"""Fresh exclusive source snapshots, actual compile/synthesis/execute, no tool install."""
from pathlib import Path
import argparse,hashlib,json,shutil,struct,subprocess,sys,traceback
HERE=Path(__file__).resolve().parent
SOURCE_FILES=['PROTOCOL.json','UPSTREAM_BINDING.json','PROSPECTIVE_BINDING.json','JOBS_CONFIG.json','jobs.txt','core_wrapper.v','controller.v','driver.cpp','sha256.hpp','generate_sources.py','audit_core.py','exact_logs.py','CORE_PROVENANCE.json','replay_portable.py','functional_oracle.py','audit_reports.py','r05_certificate_checker.py','pack_streams.py','AMENDMENTS.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def extract(p,out):
 b=p.read_bytes();assert b[:7]==b'\x7fELF\x01\x01\x01';assert struct.unpack_from('<H',b,18)[0]==243
 phoff=struct.unpack_from('<I',b,28)[0];psz,pn=struct.unpack_from('<HH',b,42)
 ram=bytearray(65536);segments=[]
 for i in range(pn):
  typ,off,va,pa,fs,ms,flags,align=struct.unpack_from('<8I',b,phoff+i*psz)
  if typ!=1:continue
  assert fs<=ms and off+fs<=len(b) and va==pa and va+ms<=8192
  ram[va:va+fs]=b[off:off+fs];segments.append(dict(address=va,file_size=fs,memory_size=ms,flags=flags))
 assert segments
 out.write_bytes(ram);return dict(elf_sha256=sha(p),ram_sha256=sha(out),segments=segments,elf_bytes=len(b))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--yosys-python-wrapper',type=Path,required=True);ap.add_argument('--zig',type=Path,required=True);ap.add_argument('--include',type=Path,required=True);ap.add_argument('--build-only',action='store_true');ap.add_argument('--resume-simulation',action='store_true');a=ap.parse_args()
 out=a.out.resolve();y=[sys.executable,'-B','-X','utf8',str(a.yosys_python_wrapper.resolve())];zig=str(a.zig.resolve());inc=a.include.resolve()
 replacements=[(str(out),'[ATTEMPT]'),(str(HERE),'[SOURCE]'),(str(a.yosys_python_wrapper.resolve()),'[YOSYS_WRAPPER]'),(zig,'[ZIG]'),(str(inc),'[YOSYS_INCLUDE]'),(sys.executable,'[PYTHON]'),(str(Path.home()),'[LOCAL_USER]')]
 def clean(s):
  for old,new in replacements:s=s.replace(old,new)
  # Tool diagnostics can normalize separators.
  for old,new in replacements:s=s.replace(old.replace('\\','/'),new)
  return s
 if a.resume_simulation:
  record=json.loads((out/'ATTEMPT.json').read_text(encoding='utf-8'));assert record['status']=='BUILT_NOT_EXECUTED'
 else:
  out.mkdir(parents=True,exist_ok=False)
  for n in SOURCE_FILES:shutil.copyfile(HERE/n,out/n)
  for n in ['firmware','upstream']:shutil.copytree(HERE/n,out/n)
  record=dict(status='IN_PROGRESS',sources={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file()},commands=[])
 def save():write(out/'ATTEMPT.json',record)
 def run(name,argv):
  save()
  try:r=subprocess.run(argv,cwd=out,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=7200)
  except Exception as e:
   record['status']='FAILED_'+name;record['commands'].append(dict(name=name,argv=[clean(x) for x in argv],exception=clean(str(e))));save();raise
  for stream in ['stdout','stderr']:(out/(name+'.'+stream+'.log')).write_text(clean(getattr(r,stream)),encoding='utf-8')
  record['commands'].append(dict(name=name,argv=[clean(x) for x in argv],returncode=r.returncode));record['status']='FAILED_'+name if r.returncode else 'IN_PROGRESS';save();print(name,r.returncode,flush=True)
  if r.returncode:raise RuntimeError('stage failed: '+name)
 if not a.resume_simulation:
  run('zig_version',[zig,'version']);run('yosys_version',y+['-V']);(out/'images').mkdir();bindings={}
  proto=json.loads((out/'PROTOCOL.json').read_text(encoding='utf-8'))
  for fn in proto['functions']:
   for flag in proto['flags']:
    name=fn+'_'+flag
    cmd=[zig,'cc','-target','riscv32-freestanding','-mcpu=generic_rv32','-mabi=ilp32','-mno-relax','-'+flag,'-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-sanitize=all','-nostdlib','-rtlib=none','-g0','-Wl,--gc-sections','-Wl,-T,firmware/link.ld','firmware/startup.S','firmware/'+fn+'.c','-o','images/'+name+'.elf']
    run('firmware_'+name,cmd);bindings[name]=extract(out/'images'/ (name+'.elf'),out/'images'/(name+'.ram'))
  write(out/'FIRMWARE_BINDINGS.json',bindings)
  run('synthesize_core',y+['-p','read_verilog upstream/picorv32.v core_wrapper.v; hierarchy -check -top core_wrapper; prep -top core_wrapper; check -assert; write_cxxrtl core.cpp'])
  run('synthesize_controller',y+['-p','read_verilog controller.v; hierarchy -check -top controller; prep -top controller; check -assert; write_cxxrtl controller.cpp'])
  run('compile_cxxrtl',[zig,'c++','-std=c++17','-O3','-UNDEBUG','-I',str(inc),'-I',str(inc/'backends/cxxrtl/runtime'),'driver.cpp','-o','simulate.exe'])
  record['status']='BUILT_NOT_EXECUTED';record['generated_sources']={n:sha(out/n) for n in ['core.cpp','controller.cpp']};save()
  if a.build_only:return
 run('functional_oracle',[sys.executable,'-B','-X','utf8','functional_oracle.py','--attempt','.'])
 run('simulation',[str(out/'simulate.exe'),'.','.'])
 run('graph_audit',[sys.executable,'-B','-X','utf8','audit_reports.py','--attempt','.'])
 run('pack_streams',[sys.executable,'-B','-X','utf8','pack_streams.py','--attempt','.'])
 record['status']='EXECUTED_AND_PRODUCER_AUDITED_PENDING_INDEPENDENT_GATE';record['outputs']={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file() and p.suffix.lower() not in ['.exe','.pdb'] and p.name!='ATTEMPT.json'};save()
if __name__=='__main__':main()
