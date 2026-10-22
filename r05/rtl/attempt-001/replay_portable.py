"""Rebuild and execute generated CXXRTL in a fresh directory, preserving failures."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,traceback
HERE=Path(__file__).resolve().parent
SOURCES=['PROTOCOL.json','reference.v','driver.cpp','generate_inputs.py','audit_core.py','CORE_PROVENANCE.json','exact_logs.py','audit_reports.py','replay_portable.py']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--yosys',default='yosys');ap.add_argument('--yosys-python-wrapper',type=Path);ap.add_argument('--cxx',default='c++');ap.add_argument('--zig',action='store_true');ap.add_argument('--include',type=Path,required=True);a=ap.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    for n in SOURCES:shutil.copyfile(HERE/n,out/n)
    y=[sys.executable,'-B','-X','utf8',str(a.yosys_python_wrapper.resolve())] if a.yosys_python_wrapper else [a.yosys]
    c=[a.cxx]+(['c++'] if a.zig else [])
    commands=[('vectors',[sys.executable,'-B','-X','utf8','generate_inputs.py','--out','vectors']),('yosys_version',y+['-V']),('synthesis',y+['-p','read_verilog reference.v; hierarchy -check -top reference_job; prep -top reference_job; check -assert; write_cxxrtl netlist.cpp']),('compiler_version',[a.cxx,'version'] if a.zig else [a.cxx,'--version']),('compile',c+['-std=c++17','-O3','-UNDEBUG','-I',str(a.include.resolve()),'driver.cpp','-o','simulate.exe']),('simulation',[str(out/'simulate.exe'),str(out/'vectors'),str(out)]),('audit',[sys.executable,'-B','-X','utf8','audit_reports.py'])]
    result=dict(kind='fresh portable new reference RTL generated compilation/execution',sources={n:sha(HERE/n) for n in SOURCES},commands=[],status='IN_PROGRESS')
    def save(): (out/'PORTABLE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    save()
    for name,cmd in commands:
        try:
            r=subprocess.run(cmd,cwd=out,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=1800)
            (out/(name+'.stdout.log')).write_text(r.stdout,encoding='utf-8');(out/(name+'.stderr.log')).write_text(r.stderr,encoding='utf-8')
            result['commands'].append(dict(name=name,argv=cmd,returncode=r.returncode));result['status']='FAILED_'+name.upper() if r.returncode else 'IN_PROGRESS';save();print(name,r.returncode,flush=True)
            if r.returncode:return r.returncode
        except Exception:
            (out/(name+'.exception.log')).write_text(traceback.format_exc(),encoding='utf-8');result['commands'].append(dict(name=name,argv=cmd,exception=traceback.format_exc()));result['status']='FAILED_'+name.upper();save();raise
    result['status']='PASS_EXECUTED_GENERATED_REFERENCE_RTL_AND_AUDIT_PENDING_INDEPENDENT_GATE';result['outputs']={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file() and p.name!='PORTABLE_REPLAY.json'};save();return 0
if __name__=='__main__':raise SystemExit(main())
