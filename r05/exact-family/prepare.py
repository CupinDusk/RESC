"""Prospectively fixed synthetic inputs and minimally adapted own benchmark."""
from pathlib import Path
import difflib, hashlib, json, random

HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / 'r04-analysis/hopper-end-to-end'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    assert not (HERE/'INPUT_MANIFEST.json').exists()
    core=(OLD/'core.hpp').read_text(encoding='utf-8')
    assert core.count('std::array<Rect,8>')==1
    newcore=core.replace('std::array<Rect,8>','std::array<Rect,48>')
    (HERE/'core.hpp').write_text(newcore,encoding='utf-8')
    cpp=(OLD/'benchmark.cpp').read_text(encoding='utf-8')
    replacements={
        'np==870&&ns==51':'np==15&&ns==15',
        'nr==9*51*3':'nr==9*15*4',
        'for(int q:{1,48,192})':'for(int q:{1,48,192,768})',
        'std::array<uint64_t,3>':'std::array<uint64_t,4>',
        'q==1?0:q==48?1:2':'q==1?0:q==48?1:q==192?2:3',
        'b.q==1?0:b.q==48?1:2':'b.q==1?0:b.q==48?1:b.q==192?2:3',
        'complete_batch_hashes=153':'complete_batch_hashes=60',
    }
    newcpp=cpp
    for a,b in replacements.items():
        assert a in newcpp,a
        newcpp=newcpp.replace(a,b)
    (HERE/'benchmark.cpp').write_text(newcpp,encoding='utf-8')
    diff=''.join(difflib.unified_diff(core.splitlines(True),newcore.splitlines(True),fromfile='R04/core.hpp',tofile='R05/core.hpp'))
    diff+=''.join(difflib.unified_diff(cpp.splitlines(True),newcpp.splitlines(True),fromfile='R04/benchmark.cpp',tofile='R05/benchmark.cpp'))
    (HERE/'SOURCE_DIFF.patch').write_text(diff,encoding='utf-8')
    plans=[];repeats={4:100,8:20,16:5,32:2,64:1}
    for n in [4,8,16,32,64]:
        for family in ['first','last','all']:
            order=list(range(n))
            starts={'first':[0],'last':[n-2],'all':list(range(0,n,2))}[family]
            for a in starts:order[a],order[a+1]=order[a+1],order[a]
            rank={a:r for r,a in enumerate(order)}
            rectangles=[];queries=[]
            for k in range(48):
                slope=(32+k%5)*(1 if k%2==0 else -1)
                width=1+k%4
                theta=[rank[i]*(1+k%3) for i in range(n)]
                x=[theta[i]+slope*(i+1) for i in range(n)]
                rectangles.append(dict(l=[v-width for v in x],u=[v+width for v in x],theta=theta,slope=slope))
                queries.append([k,abs(slope)])
            idx=len(plans)
            plans.append(dict(id=idx,stratum=idx,n=n,family=family,order=order,
                positions=list(range(1,n+1)),edges=list(zip(order[:-1],order[1:])),
                expected_exact=True,rectangles=rectangles,queries=queries,repeats=repeats[n]))
    (HERE/'inputs.json').write_text(json.dumps(plans,indent=2)+'\n',encoding='utf-8')
    lines=['15 15']
    for p in plans:
        lines.append(f"{p['id']} {p['stratum']} {p['n']} {len(p['edges'])} 1")
        lines.append(' '.join(map(str,p['positions'])))
        lines.extend(f'{a} {b}' for a,b in p['edges'])
        for r in p['rectangles']:
            lines.append(' '.join(map(str,r['l'])))
            lines.append(' '.join(map(str,r['u'])))
        lines.extend(f'{i} {d}' for i,d in p['queries'])
    lines.extend(f"{p['id']} {p['repeats']} 1 {p['id']}" for p in plans)
    (HERE/'inputs.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    rng=random.Random(20261025);schedule=[]
    for block in range(9):
        for p in plans:
            qs=[1,48,192,768];rng.shuffle(qs)
            for q in qs:
                routes=list(range(4));rng.shuffle(routes)
                schedule.append(dict(block=block,stratum=p['id'],queries=q,routes=routes))
    (HERE/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n',encoding='utf-8')
    (HERE/'schedule.txt').write_text(str(len(schedule))+'\n'+''.join(' '.join(map(str,[r['block'],r['stratum'],r['queries'],*r['routes']]))+'\n' for r in schedule),encoding='utf-8')
    names=['PROTOCOL.md','prepare.py','core.hpp','benchmark.cpp','SOURCE_DIFF.patch','inputs.json','inputs.txt','schedule.json','schedule.txt']
    manifest=dict(status='FROZEN_BEFORE_VALIDATION_AND_SINGLE_TIMING_COLLECTION',plans=15,distinct_queries=720,
        paired_blocks=9,timed_records=2160,source_binding={n:sha(OLD/n) for n in ['core.hpp','benchmark.cpp']},
        files={n:sha(HERE/n) for n in names},scope='Deliberately favorable synthetic exact family; not a representative workload.')
    (HERE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['files','source_binding']}))

if __name__=='__main__':main()
