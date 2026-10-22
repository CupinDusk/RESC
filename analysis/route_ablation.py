from pathlib import Path
from collections import Counter,defaultdict
import csv,hashlib,json
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'expected'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return {(r['case'],r['fraction']):r for r in csv.DictReader(f)}
def main():
    out=HERE/'ROUTE_ABLATION_RESULTS.json';assert not out.exists()
    p=OLD/'HOPPER_R14_ALL_AUDITOR_ROUTES.csv';q=OLD/'HOPPER_R16_ALL_QUARTET_ROUTES.csv'
    a,b=read(p),read(q);assert a.keys()==b.keys() and len(a)==384480
    budgets=defaultdict(Counter);overall=Counter()
    for key,r in a.items():
        s=b[key];assert r['exact_decision']==s['decision']
        c=budgets[key[1]];c['queries']+=1
        rejected=r['universal4_route']=='marginal_reject'
        assert rejected==(s['route']=='marginal_reject')==(r['ranking_specific_route']=='marginal_reject')
        if rejected:c['beta_reject']+=1;continue
        c['beta_survivors']+=1
        isadmit=lambda v:v not in ['graph_fallback','marginal_reject']
        f=isadmit(r['universal4_route']);qt=s['route']=='exact_marginal_admit';full=isadmit(r['ranking_specific_route'])
        if f or qt or full:assert r['exact_decision']=='admit'
        assert not(f or qt) or full
        for label,z in [('factor4',f),('quartet',qt),('union',f or qt),('full_factor',full)]:c[label+'_scalar_admit' if z else label+'_graph']+=1
        c['union_extra_over_factor4']+=qt and not f
        c['factor4_extra_over_quartet']+=f and not qt
        c['both_admit']+=f and qt
    for c in budgets.values():
        assert c['queries']==64080 and c['union_graph']<=c['factor4_graph'] and c['union_graph']<=c['quartet_graph']
        overall.update(c)
    result=dict(result='PASS_ALL_JOINED_CERTIFIED_ROUTE_ABLATIONS',protocol_sha256=sha(HERE/'ROUTE_ABLATION_PROTOCOL.json'),
       script_sha256=sha(Path(__file__)),input_sha256={x.name:sha(x) for x in [p,q]},
       budgets={k:dict(v) for k,v in sorted(budgets.items(),key=lambda kv:float(kv[0]))},total=dict(overall),
       scope=json.loads((HERE/'ROUTE_ABLATION_PROTOCOL.json').read_text())['scope'])
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result['budgets'],indent=2));print(json.dumps(dict(overall)))
if __name__=='__main__':main()
