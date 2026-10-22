"""Only generate the prospectively declared vectors; no result-dependent input."""
from pathlib import Path
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    p=json.loads((HERE/'PROTOCOL.json').read_text(encoding='utf-8'))
    cases=[]
    for vi,v in enumerate(p['vectors_v']):
        for pn,ds in p['divider_paths'].items():
            cases.append(dict(case_id=len(cases),vector_id=vi,path_name=pn,v=v,N=[2000+x for x in v],D=ds))
    invalid=[]
    for f in p['invalid_families']:
        key=('quiet_edges_before_start' if f['reason']==1 else 'change_at_subsequent_reference_edge' if f['reason']==4 else 'quiet_edges_after_command_reset')
        for x in f[key]:
            invalid.append(dict(invalid_id=len(invalid),**{k:v for k,v in f.items() if k!=key},**{key:x}))
    assert len(cases)==32 and len(invalid)==12
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'INPUTS.json').write_text(json.dumps(dict(valid=cases,invalid=invalid),indent=2)+'\n',encoding='utf-8')
    with (a.out/'vectors.txt').open('w',encoding='ascii',newline='\n') as o:
        o.write(str(len(cases))+'\n')
        for c in cases:o.write(' '.join(map(str,[c['case_id'],c['vector_id'],*c['N'],*c['D']]))+'\n')
        o.write(str(len(invalid))+'\n')
        for f in invalid:
            quiet=f.get('quiet_edges_before_start',0) if f['reason']==1 else f.get('quiet_edges_after_command_reset',2)
            o.write(' '.join(map(str,[f['invalid_id'],f['reason'],f['N'],f['D'],quiet,f.get('change_at_subsequent_reference_edge',0),f.get('changed_D',f['D'])]))+'\n')
    manifest={'protocol_sha256':hashlib.sha256((HERE/'PROTOCOL.json').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'files':{n:hashlib.sha256((a.out/n).read_bytes()).hexdigest() for n in ['INPUTS.json','vectors.txt']}}
    (a.out/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
