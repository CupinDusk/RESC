"""Write bounded paper facts and the independent evidence manifest."""
from pathlib import Path
import hashlib,json,sys,shutil
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def main():
    graph=load(HERE/'GRAPH_AND_FRAMING_CHECK.json');producer=load(HERE/'PRODUCER_EDGE_CHECK.json');fresh=load(HERE/'FRESH_EDGE_CHECK.json');mutants=load(HERE/'MUTANT_RESULTS.json')
    assert graph['status']==producer['status']==fresh['status']==mutants['status']=='PASS'
    assert producer==fresh
    limitations=[
      'Author-side independent validation, not a blind review and not a conference judgment.',
      'New logical reference RTL and synchronous reference ticks only; no native Hopper/H20/HUSH, GPU, silicon, FPGA, physical clock calibration, CDC/metastability, PPA, latency, or performance validation.',
      'All 32 designed reports and 23,072 graph queries are a fixed census, not workload frequencies or a representative distribution; all-tie admissions dominate the true-order population.',
      'Admission is feasibility of a real-valued log abstraction; it does not identify the original private N, prove concrete alternate integer N/D RTL realizability, or provide cryptographic/inference-resistant privacy.',
      'Source trust still includes truthful guard/obligation bits and the timer interface. Full debug evidence intentionally discloses N/D, while the audited interface excludes them.',
      'Reset initializes the synchronous model; pre-reset CXXRTL zero values are recorded but are not a hardware initialization guarantee. Logical settlement means two stable quiet sampled edges, not analog settling.',
      'The explicit full-edge oracle uses signed int64 trace storage and is valid on the declared bounded runs; it is not a proof for arbitrary uint64 overflow states.',
      'Declared maximum N=2100, D=1030, N*D<=2163000 makes all 32-bit counters, 64-bit timer, and 40-bit products nonoverflowing. Overflow reason7 was source-reviewed but not forced by simulation. The small independent harness additionally exercised zero inputs (reason6), busy reset (reason5), and repeated busy start (reason8), without adding them to the 12 declared controls.',
      'The generated executable is not byte-identical even after PE timestamps alone: CodeView RSDS build GUID bytes also differ. Its .text section and all semantic outputs are exact; the GUID difference is preserved and not ignored.',
      'The gzip query archives have different mtime bytes and actual SHA256 bindings; their decompressed bytes are exact. No archive byte-identity or fully deterministic-build claim is made.',
      'Independent finite-census/certificate verification and state induction do not constitute a general formal proof of arbitrary RTL/compiler/toolchain behavior.'
    ]
    facts=dict(status='PASS_FOR_BOUNDED_LOGICAL_REFERENCE_RTL_AND_REAL_LOG_ABSTRACTION',reports=32,jobs=192,invalid_controls=12,decoded_edges_per_trace=producer['decoded_edges'],independently_decoded_traces=2,valid_active_edges=producer['valid_active_edges'],valid_job_pulses=producer['valid_pulses'],total_order_queries=23040,fixed_partial_queries=32,all_query_certificates_checked=23072,numeric_unknown=0,semantic_mutants_synthesized_compiled_detected=5,totals=graph['totals'],per_case=graph['per_case'],per_vector_total=graph['per_vector_total'],per_vector_partial=graph['per_vector_partial'],changed_partial_case_ids=graph['changed_partial_case_ids'],incremental_rejection_denominators=dict(total_order_box_admissions=8940,total_order_non_tie_box_admissions=6060,total_order_false_box_admissions=6032,additional_total_rejections=76,partial_box_admissions=20,partial_false_box_admissions=16,additional_partial_rejections=6),limitations=limitations,source_sha256={n:sha(BASE/n) for n in ['PROTOCOL.json','reference.v','driver.cpp','audit_core.py','exact_logs.py','audit_reports.py']},evidence=['GRAPH_AND_FRAMING_CHECK.json','PRODUCER_EDGE_CHECK.json','FRESH_EDGE_CHECK.json','MUTANT_RESULTS.json','fresh-replay/PORTABLE_REPLAY.json'])
    save(HERE/'PAPER_READY_FACTS.json',facts)
    table=['| Population | Queries | True admitted | False admitted | Joint rejected | Box rejected | Extra joint rejections | Unknown |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for key,name in [('total','All total orders'),('tie_total','All-tie total orders'),('other_total','Other-vector total orders'),('partial','All fixed conjunctions'),('tie_partial','All-tie fixed conjunctions'),('other_partial','Other-vector fixed conjunctions')]:
        c=graph['totals'][key];table.append(f"| {name} | {c['reports']} | {c['true_admit']} | {c['false_admit']} | {c['reject']} | {c['box_reject']} | {c['box_admit_path_reject']} | {c['unknown']} |")
    vector=['| Vector | True total orders | Admitted | Rejected | Box rejected | Extra rejections |','|---|---:|---:|---:|---:|---:|']
    for key,c in graph['per_vector_total'].items():vector.append(f"| {key} | {c['true']} | {c['admit']} | {c['reject']} | {c['box_reject']} | {c['box_admit_path_reject']} |")
    paper='''# Independently validated paper facts

PASS for the declared logical reference RTL and real-valued log abstraction.
This is author-side independent validation, not a blind review or score.

Actual Yosys 0.70 synthesis and Zig 0.14.1 C++17 compilation were rerun in
`fresh-replay/`. A separately written oracle explicitly expanded and checked
all 389,022,846 post-edge states in each of the original and fresh traces.
The census contains 32 valid reports, 192 jobs, 387,019,984 valid active ticks,
386,440 valid job pulses, and 12 exact-reason contract-unknown controls.
Every valid job completed after exactly N*D subsequent reference rising edges;
the start edge is excluded. The reported timers came from generated RTL.

All 23,040 total orders and all 32 fixed P<=F/A<=S conjunctions were recomputed
using 13 original z=-theta and bias variables with an independent edge-list
algorithm. Exact Fraction log sums and geometric tail bounds supplied separate
10^70 outward bounds. All 8,878 admitted witnesses were checked in the original
variables, including direct rigorous real-log comparisons. Every one of the
14,194 relaxed negative cycles was checked edge by edge with its exact weights.

'''+ '\n'.join(table)+'''

The 2,880 all-tie true total orders account for most of the 2,908 true orders;
the other seven vectors contribute 28. No true claim was rejected or unknown.
The extra total-order rejection count is 76 among 8,940 box admissions, or
among 6,060 after excluding all ties; 6,032 box admissions are originally
false. The extra fixed-conjunction count is 6 among 20 box admissions, 16 of
which are false. These are designed-census denominators, not workload rates.
The changed fixed-conjunction case IDs are 0, 2, 15, 26, 27, 28.

'''+ '\n'.join(vector)+'''

Vectors 1, 4, and 5 have zero incremental total-order rejection. All 32 per-case
tables, including every zero cell, are in PAPER_READY_FACTS.json.

Admission means feasibility in the licensed real-valued log abstraction. It
does not recover original N, establish an alternate concrete integer RTL
realization, or guarantee secrecy against timing inference. A rejection
refutes the queried conjunction for any concrete source state mapping into
that abstraction under the trusted source obligations.

The five actually synthesized and compiled semantic mutants widened the guard,
removed held-divider checking, shortened the countdown, removed the reset
license, or removed the settlement gate. The independent harness detected all
five, while its unmodified RTL baseline passed.

The replay is semantically exact, not wholly byte-identical. Gzip mtime bytes
and the resulting archive binding differ. The executable differs in PE
timestamps and CodeView RSDS build GUID bytes; no GUID bytes are silently
ignored. Its .text section, generated netlist, all sampled trace bytes, all
jobs/intervals/observations and decompressed graph records are exact. Both
actual archive hashes and binary differences are retained in the evidence.

'''+ '\n'.join('- '+x for x in limitations)+'\n'
    (HERE/'PAPER_READY_FACTS.md').write_text(paper,encoding='utf-8')
    audit='''# Independent author-side validation

**PASS**, bounded to the declared new logical reference RTL and real log
abstraction. There is no native H20, physical clock, PPA, performance or
publication result. Producer evidence is unchanged: all 77 delivered inventory
entries still match their exact sizes and SHA256 values, including attempt-001
and its missing-runtime-header compilation failure.

## What was independently checked

1. The frozen protocol, source contracts, schema, source code, all attempt-002
   artifacts, provenance and actual command records were inspected. No reviews
   or manuscripts were consulted. The copied audit_core.py hash is
   9a4ad638a45cd69b43e7b2389417d6a43481225ee2c6e67fd9664b58d31f55a9.
2. Fresh actual Yosys synthesis and generated CXXRTL compilation/execution used
   the portable producer runner under independent/fresh-replay. This alone was
   not the independent gate. edge_oracle.cpp, independent_checks.py and
   mutant_harness.cpp are separately written and import no producer checker.
3. edge_oracle.cpp explicitly expands every RLE span (1,166,181 rows per trace)
   into all 389,022,846 sampled states. Every output register is compared to
   its independently computed next state on every edge, including reset,
   license, two quiet settlement edges, both guard inequalities, held divider,
   remaining/phase/pulses, timer, jobpulse, completion and reason priority.
4. independent_checks.py reconstructs every input control segment from the
   frozen protocol, not from producer job labels, and checks every affine input
   span against that schedule. All 192 job rows and all 12 invalid rows match
   independently derived values in every column. This binds actual private
   latched cycle counts to the fixed vectors, changing cfgn=N+777 after capture,
   actual completion edges, and integer [T-1,T+1] intervals. All scenarios,
   initial vectors, field framing, edge contiguity and no-loss census are checked.
5. The audited interface has an exact field whitelist. No N,D, phases, pulse
   counts, truth or vector labels enter it. Intervals and validity bits are
   bound back to decoded jobs. Invalid controls have a null interval and no
   graph permission; all 12 produce their designated reason, with family counts
   3 missing reset, 2 unsettled, 3 invalid guard and 4 busy divider changes.
6. All graph inputs after interface construction come only from that interface.
   Producer N is used solely for separate truth annotation. An independent
   13-variable original-state difference-constraint graph is solved using
   synchronous edge-list Bellman-Ford; it does not call or import the producer
   six-node matrix/Bellman-Ford/Floyd implementation. Independent exact Fraction
   logarithms use 170 terms, rational arithmetic and a geometric remainder,
   with 10^70 outward graph endpoints. Every supplied 10^60 enclosure contains
   the separately certified true log interval. All 23,072 statuses, box beta
   fractions, true/false annotations, group/per-vector/per-case counts and all
   certificates match. Zero and no-improvement cells are retained.
7. For admissions the original theta,bias witness satisfies every observation,
   guard step and query, including direct comparisons against separately
   enclosed real logarithms. For rejection, every cycle is closed, every edge
   weight is independently derived from the observation plus bias-distance
   bound (or the queried zero-order edge), and the exact sum is negative.
8. Six extra actual RTL builds comprise the independent baseline and five
   semantic mutants, each synthesized, compiled, executed and logged. All five
   mutants are killed at a contract-observable post-edge state; baseline passes.
   These are not file-difference or compile-failure tests. They use the same
   independent transition oracle as full-trace validation.

## Induction and source-level argument

Synchronous report reset writes every RTL register and previous_D=1000. The
pre-reset simulator vector is only a decoding origin. Idle command reset
captures N,D, clears counters and settlement, grants one license, and preserves
guard history. Two subsequent quiet edges at the captured D establish the
logical settled state. Start consumes the license even on rejection. For an
accepted start, phase=pulses=timer=0 and remaining=N, with busy and valid true.
The guarded history update makes both exact inequalities equivalent to
|log(D_j/1000)-log(D_(j-1)/1000)|<=log(201/200), including the initial D0=1000.

For k subsequent valid busy edges, induct on divider phase: a nonpulse edge
increments phase and timer; phase=D-1 emits exactly one jobpulse, clears phase,
increments pulses and decrements remaining. Therefore timer=k, phase=k mod D,
pulses=floor(k/D), remaining=N-floor(k/D), until k=N*D. The Nth pulse makes
remaining=0,busy=0,done=1. This is the first completion and the timer was counted
on actual RTL edges, not assigned a product. All 192 full edge sequences match
this argument and use a stable held divider despite the changed cfgn input.

N in [1996,2100], D in [976,1030] and ND<=2,163,000 are independently bound to
the protocol and actual edges. Phase<D, pulses<=N and remaining>=0 preclude
wraparound. All declared guard products are below 201*1030<2^40. The 32-bit
count and 64-bit timer cannot overflow here. A configured-divider change has
priority over counting or completion and returns reason4; no invalid attempt
licenses an observation. Busy reset, repeated start, zero inputs and overflow
branches were source-reviewed; only the first three were additionally exercised
in the small independent harness. Overflow injection is outside this evidence.

For graph equivalence, write z_i=-theta_i. Each observation is the pair of
edges b_(i+1)-z_i<=u_i and z_i-b_(i+1)<=-l_i, adjacent bias edges have weight
delta in each direction, and theta_p<=theta_q is z_q-z_p<=0. All 13 variables
can be translated together to make b0=0 without changing these constraints.
The producer six-node eliminated weights upper_b-lower_a+delta*|a-b| are the
corresponding necessary pairwise bounds, and its constructive Lipschitz bias
witness restores the original constraints on admission. The independent graph,
original-variable witness checks and edgewise cycles validate all critical
producer matrix, feasibility, anchoring, beta and certificate logic on this
declared census. This is not a universal formal proof of the software.

## Retained failures and replay nonidentity

The producer attempt-001 remains byte-exact: actual synthesis succeeded and
compilation failed because cxxrtl/cxxrtl.h required the runtime include root.
The independent replay supplies both include roots and no RTL/input edit.

Independent check attempt-001 first stopped at an overly strong whole-file
AUDIT_RESULTS byte-equality assertion. Investigation showed gzip mtime at
offsets 4,5 changed its actual archive hash, and only that binding changed in
AUDIT_RESULTS. Independent attempt-002 then stopped at an executable-equality
assertion: the PE timestamps and CodeView RSDS build GUID differ. Both failed
check logs are preserved. The final checker does not suppress these facts or
normalize the GUID: it records exact differences, validates each actual hash,
requires .text/code and all semantic outputs exact, and separately reports
whole-file byte inequality. Checks attempt-003 and final attempt-004 pass.
No producer source, output, manifest or failure evidence was repaired.

The archives' decompressed query records are byte-exact. Executables differ
only in parsed PE timestamp fields and RSDS GUID bytes; .text section SHA256
is 854ab5c540ef3b64d7e3e1ac1d3f5fea4d8b7dff9d1fbc1390df6c0d4446682d.
The exact 17 executable byte offsets and both actual archive hashes are in
GRAPH_AND_FRAMING_CHECK.json. A deterministic package/build claim is not made.

## Scope and limitations

'''+ '\n'.join('- '+x for x in limitations)+'''

All outputs of this validation are under independent/. No remote data, native
private code, reviewers, manuscript, publication, push or global installation
was used or modified. No CPU performance timings were collected. Reproduction
commands and actual per-stage logs are in COMMANDS.json, fresh-replay's
PORTABLE_REPLAY.json and each mutants/*/RESULT.json.
'''
    (HERE/'INDEPENDENT_AUDIT.md').write_text(audit,encoding='utf-8')
    record=dict(status='PASS',gate='Bounded logical source/trace/semantic/certificate validation',full_replay_byte_identity=False,producer_inventory_unchanged=True,independence=graph['independence'],edges=producer,graph_summary=dict(queries=graph['queries'],certificates=graph['certificates'],totals=graph['totals'],changed_partial_case_ids=graph['changed_partial_case_ids']),replay_nonidentity=dict(gzip=graph['gzip_binding'],binary=graph['binary_binding']),mutants=mutants,limitations=limitations)
    save(HERE/'INDEPENDENT_AUDIT.json',record)
    source_names=['edge_oracle.cpp','mutant_harness.cpp','independent_checks.py','run_mutants.py','record_commands.py','finalize_audit.py']
    snap=HERE/'checker-sources';snap.mkdir(exist_ok=True)
    for n in source_names:shutil.copyfile(HERE/n,snap/n)
    sources=dict(independent={n:sha(HERE/n) for n in source_names},producer={p.relative_to(BASE).as_posix():sha(p) for p in BASE.iterdir() if p.is_file()},external_runtime_header=sha(BASE.parents[3]/'.tools/iscas-rtl-20261023/yowasp_yosys/share/include/backends/cxxrtl/runtime/cxxrtl/cxxrtl.h'))
    save(HERE/'SOURCE_MANIFEST.json',sources)
    files=[dict(path=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='OUTPUT_MANIFEST.json']
    save(HERE/'OUTPUT_MANIFEST.json',dict(status='BOUND_ALL_INDEPENDENT_FILES_EXCEPT_THIS_MANIFEST',files=files))
    print('PASS final independent audit and paper facts written')
if __name__=='__main__':main()
