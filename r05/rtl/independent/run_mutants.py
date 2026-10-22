"""Actually synthesize and compile semantic RTL mutants; preserve all logs."""
from pathlib import Path
import hashlib,json,subprocess,sys,shutil
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def main():
    source=(BASE/'reference.v').read_text(encoding='utf-8')
    mutations=[('baseline',None,None),('widen_guard',"40'd201","40'd202"),('missing_held_check','if (cfgd != heldd) begin',"if (1'b0) begin"),('short_countdown','remaining <= nlatched;','remaining <= nlatched - 1;'),('missing_reset_license','if (!licensed)',"if (1'b0)"),('missing_settle_gate','else if (settled != 2 || cfgd != heldd)',"else if (1'b0)")]
    out=HERE/'mutants';out.mkdir(exist_ok=False)
    zig=ROOT/'.tools/zig-0.14.1/zig-x86_64-windows-0.14.1/zig.exe';inc=ROOT/'.tools/iscas-rtl-20261023/yowasp_yosys/share/include';y=ROOT/'.tools/run_iscas_yosys.py'
    summary=[]
    for name,old,new in mutations:
        d=out/name;d.mkdir();text=source if old is None else source.replace(old,new)
        assert old is None or text!=source
        (d/'reference.v').write_text(text,encoding='utf-8')
        for n in ['mutant_harness.cpp','edge_oracle.cpp']:shutil.copyfile(HERE/n,d/n)
        result=dict(name=name,mutation=dict(old=old,new=new),commands=[],source_hashes={n:sha(d/n) for n in ['reference.v','mutant_harness.cpp','edge_oracle.cpp']})
        commands=[('synthesis',[sys.executable,'-B','-X','utf8',str(y),'-p','read_verilog reference.v; hierarchy -check -top reference_job; prep -top reference_job; check -assert; write_cxxrtl netlist.cpp']),('compile',[str(zig),'c++','-std=c++17','-O3','-UNDEBUG','-I',str(inc),'-I',str(inc/'backends/cxxrtl/runtime'),'mutant_harness.cpp','-o','check.exe']),('execute',[str(d/'check.exe')])]
        for step,argv in commands:
            r=subprocess.run(argv,cwd=d,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
            (d/(step+'.stdout.log')).write_text(r.stdout,encoding='utf-8');(d/(step+'.stderr.log')).write_text(r.stderr,encoding='utf-8')
            result['commands'].append(dict(name=step,argv=argv,returncode=r.returncode))
            if step!='execute':assert r.returncode==0,(name,step,r.stderr)
            else:
                assert r.returncode==(0 if name=='baseline' else 1),(name,r.returncode,r.stdout,r.stderr)
                result['status']='BASELINE_PASS' if name=='baseline' else 'MUTANT_DETECTED'
        result['output_hashes']={p.name:sha(p) for p in d.iterdir() if p.is_file()}
        save(d/'RESULT.json',result);summary.append(result);print(name,result['status'],flush=True)
    save(HERE/'MUTANT_RESULTS.json',dict(status='PASS',baseline_passed=True,actually_synthesized_and_compiled_mutants=5,all_five_detected=True,cases=summary))
if __name__=='__main__':main()
