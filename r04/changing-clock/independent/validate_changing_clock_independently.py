"""Independent, exact checker of serialized changing-clock model evidence.

Reads serialized protocol/observations/results/report stream, the slot-mapping
addendum, and the prior R03 protocol mapping. The producer and its audit_core
are never opened, imported, or executed. Standard library only.
Default output is created exclusively; use --check-only for a repeat run.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SCALE = 10 ** 60
TERMS = 130
GUARD = Q(201, 200)
REFERENCE = Q(10000)
VECTORS = [
    [1000000,1010000,1006000,998000,1024000,1002000],
    [1000000,1000000,1000000,1000000,1000000,1000000],
    [1000000,1002000,1004000,1006000,1008000,1010000],
    [1010000,1008000,1006000,1004000,1002000,1000000],
    [1000000,1000500,1001000,1001500,1002000,1002500],
    [1000000,1010000,1020000,1030000,1040000,1050000],
    [1002500,1000000,1002000,1000500,1001500,1001000],
    [1024000,1010000,1006000,998000,1000000,1002000],
]
PATHS = {
    'rising': [REFERENCE * GUARD ** j for j in range(1,7)],
    'falling': [REFERENCE / GUARD ** j for j in range(1,7)],
    'alternating': [Q(10050) if j % 2 else REFERENCE for j in range(1,7)],
}
# Retained P,S,B,G,A,F slot order from the prior independent checker.
FIXED = [(0,5),(4,1)]
COUNTS = Counter()
FAILURES = []


def check(condition, label):
    COUNTS['assertions'] += 1
    if not condition:
        FAILURES.append(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))


def atanh_interval(z):
    """For 0<=z<=1/3, 2*sum z^(2k+1)/(2k+1), with exact tail."""
    assert 0 <= z <= Q(1,3)
    total = Q(0)
    power = z
    zz = z*z
    for k in range(TERMS):
        total += power / (2*k+1)
        power *= zz
    low = 2*total
    return low, low + 2*power / ((2*TERMS+1)*(1-zz))


LOG2 = atanh_interval(Q(1,3))


@lru_cache(None)
def log_interval(x):
    assert x > 0
    exponent = 0
    reduced = x
    while reduced >= 2:
        reduced /= 2
        exponent += 1
    while reduced < 1:
        reduced *= 2
        exponent -= 1
    low, high = atanh_interval((reduced-1)/(reduced+1))
    if exponent >= 0:
        return low + exponent*LOG2[0], high + exponent*LOG2[1]
    return low + exponent*LOG2[1], high + exponent*LOG2[0]


def enclosure_is_valid(x, bounds):
    low, high = log_interval(x)
    return (len(bounds) == 2 and all(type(v) is int for v in bounds)
            and Q(bounds[0],SCALE) <= low <= high <= Q(bounds[1],SCALE)
            and high-low < Q(1,10**100))


def verify_log(x, bounds, label):
    check(enclosure_is_valid(x,bounds), label)
    check(bounds[1]-bounds[0] <= 1, label + ': at most one scaled unit')
    COUNTS['serialized_log_bounds_checked'] += 1


def guard_bad_edges(path):
    previous = REFERENCE
    bad = []
    for slot, current in enumerate(path,1):
        if not (previous/GUARD <= current <= previous*GUARD):
            bad.append(slot)
        previous = current
    return bad


def report_claims(report):
    if report['kind'] == 'total_order':
        order = report['order']
        return [(a,b) for k,a in enumerate(order) for b in order[k+1:]]
    return [tuple(pair) for pair in report['claims']]


def pair_weights(obs,delta,tight):
    logs = obs['log_scaled_bounds']
    low = [p[1 if tight else 0] for p in logs['l']]
    high = [p[0 if tight else 1] for p in logs['u']]
    return [[high[j]-low[i]+abs(j-i)*delta for j in range(6)] for i in range(6)]


def negative_cycle(weights,claims):
    """Independent six-node Floyd-Warshall closure, integer arithmetic."""
    distance = [row[:] for row in weights]
    for i in range(6):
        distance[i][i] = min(distance[i][i],0)
    for a,b in claims:
        distance[b][a] = min(distance[b][a],0)
    for k in range(6):
        for i in range(6):
            for j in range(6):
                candidate = distance[i][k]+distance[k][j]
                if candidate < distance[i][j]:
                    distance[i][j] = candidate
    return any(distance[i][i] < 0 for i in range(6))


def classify(obs,claims,delta):
    relaxed = pair_weights(obs,delta[1],False)
    tight = pair_weights(obs,delta[0],True)
    if negative_cycle(relaxed,claims):
        return 'reject'
    if not negative_cycle(tight,claims):
        return 'admit'
    return 'unknown'


def all_anchor_beta(obs,claims):
    logs = obs['log_scaled_bounds']
    low = max([Q(0)] + [Q(logs['l'][a][0]-logs['u'][b][1],abs(a-b)) for a,b in claims])
    high = max([Q(0)] + [Q(logs['l'][a][1]-logs['u'][b][0],abs(a-b)) for a,b in claims])
    return low,high


def box_class(beta,delta):
    return 'admit' if beta[1] <= delta[0] else 'reject' if beta[0] > delta[1] else 'unknown'


def positive_errors(report,obs,claims,delta):
    cert = report['certificate']
    theta,bias = cert['theta_scaled'],cert['bias_scaled']
    errors = []
    if len(theta) != 6 or len(bias) != 7:
        return ['dimensions']
    if not all(type(v) is int for v in theta+bias):
        return ['integer witness']
    if bias[0] != 0:
        errors.append('anchor')
    for i in range(6):
        if not (obs['log_scaled_bounds']['l'][i][1] <= theta[i]+bias[i+1]
                <= obs['log_scaled_bounds']['u'][i][0]):
            errors.append('rectangle')
        if abs(bias[i+1]-bias[i]) > delta:
            errors.append('Lipschitz')
    if any(theta[a] > theta[b] for a,b in claims):
        errors.append('rank')
    return errors


def negative_errors(report,relaxed,claims):
    cert = report['certificate']
    cycle,weights = cert['cycle'],cert['weights']
    errors = []
    if len(cycle) != len(weights) or not cycle:
        return ['length']
    rank_edges = {(b,a) for a,b in claims}
    for k,((start,end),weight) in enumerate(zip(cycle,weights)):
        if not (type(start) is int and type(end) is int and 0 <= start < 6 and 0 <= end < 6):
            errors.append('index')
            continue
        if end != cycle[(k+1)%len(cycle)][0]:
            errors.append('continuity')
        if not (type(weight) is int and (weight == relaxed[start][end]
                or ((start,end) in rank_edges and weight == 0))):
            errors.append('edge')
    if not (sum(weights) == cert['total'] < 0):
        errors.append('negative sum')
    return errors


def contribution(report):
    status,box,truth = report['path'],report['box'],report['true']
    return Counter({
        'reports':1,status:1,'true':int(truth),
        'true_admit':int(truth and status=='admit'),
        'true_reject':int(truth and status=='reject'),
        'false_admit':int(not truth and status=='admit'),
        'box_'+box:1,
        'box_admit_path_reject':int(box=='admit' and status=='reject'),
    })


def normalized(counter):
    return {k:counter[k] for k in ('reports','admit','reject','unknown','true','true_admit',
        'true_reject','false_admit','box_admit','box_reject','box_unknown','box_admit_path_reject')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--output',default='VALIDATION.json')
    args = parser.parse_args()
    protocol = read_json('PROTOCOL.json')
    mapping_addendum = read_json('SLOT_MAPPING_ADDENDUM.json')
    prior_protocol_path = BASE.parent.parent/'r03-analysis'/'hopper-clock'/'PROTOCOL.json'
    prior_mapping = json.loads(prior_protocol_path.read_text(encoding='utf-8'))['slots']
    observations = read_json('OBSERVATIONS.json')
    results = read_json('RESULTS.json')
    with gzip.open(BASE/'ALL_REPORTS.jsonl.gz','rt',encoding='utf-8') as stream:
        reports = [json.loads(line) for line in stream if line.strip()]
    check(protocol['reference_multiplier']==10000,'declared reference')
    check(Q(protocol['ratio_guard'])==GUARD,'declared guard')
    check(protocol['slots']==list(range(1,7)),'declared slots')
    check(protocol['cycle_count_vectors']==VECTORS,'all eight predeclared vectors')
    check(set(protocol['legal_paths'])==set(PATHS),'three predeclared path names')
    check(protocol['legal_paths']=={
        'rising':'M_j=10000*(201/200)^j for j=1..6',
        'falling':'M_j=10000*(200/201)^j for j=1..6',
        'alternating':'M_j=10050 for odd j and 10000 for even j'},'predeclared exact path formulas')
    expected_mapping = dict(zip('PSBGAF',range(1,7)))
    check(prior_mapping==expected_mapping,'prior R03 explicit name-to-slot mapping')
    check(mapping_addendum['mapping_inherited_from_R03']==prior_mapping,'addendum matches independently read prior mapping')
    check(mapping_addendum['inherited_source']=='r03-analysis/hopper-clock/PROTOCOL.json','addendum source identity')
    check('after generation' in mapping_addendum['status'],'mapping repair honestly dated after generation')
    check(FIXED==[(prior_mapping['P']-1,prior_mapping['F']-1),(prior_mapping['A']-1,prior_mapping['S']-1)],
          'fixed clauses derived from named prior slots')
    check(int(results['scale'])==SCALE,'declared numerical scale')
    delta = results['delta_scaled_enclosure']
    verify_log(GUARD,delta,'guard logarithm')
    check(len(observations)==8*3,'24 path-specific observation cases')
    check(len(reports)==8*3*(720+1),'17304 audit reports, excluding failed-contract control')
    by_id = {}
    seen_observations = set()
    for obs in observations:
        case,vector,path_name = obs['case_id'],obs['vector_id'],obs['path_name']
        check(type(case) is int and case not in by_id,'unique integer case ID')
        by_id[case] = obs
        check((vector,path_name) not in seen_observations,'unique vector/path observation')
        seen_observations.add((vector,path_name))
        check(case==3*vector+list(PATHS).index(path_name),'canonical case numbering')
        check(obs['cycles']==VECTORS[vector],'cycle vector identity')
        multipliers = [Q(v) for v in obs['multipliers']]
        check(multipliers==PATHS[path_name],'exact rational multiplier sequence')
        check(not guard_bad_edges(multipliers),'legal controller guard')
        previous = REFERENCE
        for i,(cycles,multiplier) in enumerate(zip(VECTORS[vector],multipliers)):
            check(max(multiplier/previous,previous/multiplier)==GUARD,
                  f'case {case} edge {i+1}: exact guard attainment')
            previous = multiplier
            COUNTS['guard_edges_checked'] += 1
            duration = Q(cycles)*REFERENCE/multiplier
            check(Q(obs['durations'][i])==duration,f'case {case} slot {i+1}: reset/hold duration')
            lower = duration.numerator//duration.denominator-1
            upper = -(-duration.numerator//duration.denominator)+1
            check(Q(obs['lower'][i])==lower and Q(obs['upper'][i])==upper,
                  f'case {case} slot {i+1}: own-path floor/ceil rectangle')
            check(0 < lower <= duration <= upper and upper-lower in (2,3),
                  f'case {case} slot {i+1}: positive timer enclosure')
            check(len(str(duration.numerator))<=50 and len(str(duration.denominator))<=50,
                  'duration within declared rational precision domain')
            verify_log(Q(lower),obs['log_scaled_bounds']['l'][i],f'case {case} slot {i+1}: lower logarithm')
            verify_log(Q(upper),obs['log_scaled_bounds']['u'][i],f'case {case} slot {i+1}: upper logarithm')
            COUNTS['exact_rational_durations_checked'] += 1
            COUNTS['path_specific_timer_rectangles_checked'] += 1
    check(set(by_id)==set(range(24)),'all 24 case IDs')
    check(seen_observations=={(v,p) for v in range(8) for p in PATHS},'complete vector/path coverage')
    seen_orders = set()
    seen_partials = set()
    all_counts,total_counts,partial_counts = Counter(),Counter(),Counter()
    case_counts = {case:Counter() for case in by_id}
    graph_cache = {case:(pair_weights(obs,delta[0],True),pair_weights(obs,delta[1],False))
                   for case,obs in by_id.items()}
    boundary_distances = []
    for report in reports:
        case = report['case_id']
        obs = by_id[case]
        claims = report_claims(report)
        if report['kind']=='total_order':
            order = tuple(report['order'])
            check(sorted(order)==list(range(6)),'order is permutation')
            check((case,order) not in seen_orders,'no duplicated order')
            seen_orders.add((case,order))
            check(len(claims)==15,'all 15 transitive total-order pairs')
        else:
            check(report['kind']=='fixed_partial','declared report kind')
            check(case not in seen_partials,'one fixed partial per case')
            seen_partials.add(case)
            check(claims==FIXED,'fixed P<=F,A<=S index clauses')
            check(report==obs['fixed_partial'],'observation partial byte-value cross-reference')
        truth = all(obs['cycles'][a] <= obs['cycles'][b] for a,b in claims)
        check(type(report['true']) is bool and report['true']==truth,'truth from original integer Ni with ties')
        tight,relaxed = graph_cache[case]
        relaxed_bad,tight_bad = negative_cycle(relaxed,claims),negative_cycle(tight,claims)
        COUNTS['independent_floyd_closures'] += 2
        status = 'reject' if relaxed_bad else 'admit' if not tight_bad else 'unknown'
        check(report['path']==status,'independent interval-safe audit classification')
        check(not truth or status=='admit','every true report admitted')
        if status=='admit':
            check(not positive_errors(report,obs,claims,delta[0]),'original-variable admitted certificate')
            COUNTS['positive_original_variable_certificates'] += 1
            COUNTS['positive_rectangle_checks'] += 6
            COUNTS['positive_Lipschitz_checks'] += 6
            COUNTS['positive_ranking_checks'] += len(claims)
        elif status=='reject':
            check(not negative_errors(report,relaxed,claims),'relaxed negative-cycle certificate edgewise')
            COUNTS['negative_cycle_certificates'] += 1
            COUNTS['negative_cycle_edges'] += len(report['certificate']['cycle'])
            COUNTS['negative_cycle_sum_checks'] += 1
        beta = all_anchor_beta(obs,claims)
        check(beta==(Q(report['beta_lower']),Q(report['beta_upper'])),'all-real-anchor beta bounds')
        check(box_class(beta,delta)==report['box'],'conservative box threshold')
        if report['box']=='admit':
            boundary_distances.append(delta[0]-beta[1])
        elif report['box']=='reject':
            boundary_distances.append(beta[0]-delta[1])
        counts = contribution(report)
        all_counts.update(counts)
        if report['kind']=='total_order':
            total_counts.update(counts)
            case_counts[case].update(counts)
        else:
            partial_counts.update(counts)
        COUNTS['report_truth_checks'] += 1
        COUNTS['box_threshold_checks'] += 1
    expected = {(case,order) for case in range(24) for order in permutations(range(6))}
    check(seen_orders==expected,'complete exact 24*720 order enumeration')
    check(seen_partials==set(range(24)),'complete 24 fixed-partial enumeration')
    for case,obs in by_id.items():
        for key,recorded in obs['total_order_summary'].items():
            check(case_counts[case][key]==recorded,f'case {case} summary {key}')
    for key,recorded in results['total_order_summary'].items():
        check(total_counts[key]==recorded,'RESULTS total-order summary '+key)
    check(results['legal_cases']==24 and results['reports']==len(reports),'RESULTS population counts')
    check(results['guard_checks']==COUNTS['guard_edges_checked']==144,'RESULTS guard check count')
    check(results['guard_attaining_edges']==COUNTS['guard_edges_checked'],'RESULTS guard attainment count')
    check(results['positive_certificates']==COUNTS['positive_original_variable_certificates'],'RESULTS admission count')
    check(results['negative_certificates']==COUNTS['negative_cycle_certificates'],'RESULTS rejection count')
    check(results['numeric_unknown']==all_counts['unknown'],'RESULTS numeric unknown count')
    check(all_counts['true_reject']==0 and all_counts['true_admit']==all_counts['true'],'all true reports admitted aggregate')

    # Contract dispatch is independently evaluated before either graph routine.
    bad_path = [Q(x) for x in (10000,10060,10000,10000,10000,10000)]
    bad_edges = guard_bad_edges(bad_path)
    check(bad_edges==[2,3],'failed controller edges are exactly 2 and 3')
    contract_counts = Counter()
    for unused_vector in VECTORS:
        for unused_order in list(permutations(range(6)))+[None]:
            decision = 'contract-unknown' if guard_bad_edges(bad_path) else 'audit-permitted'
            contract_counts[decision] += 1
    check(contract_counts==Counter({'contract-unknown':8*721}),'5768 control reports stop before audit')
    control = results['contract_negative_control']
    check([Q(x) for x in control['multipliers']]==bad_path,'negative-control multipliers')
    check(control['bad_edges']==bad_edges,'negative-control bad-edge summary')
    check(control['vectors']==8 and control['reports_per_vector']==721 and control['contract_unknown']==5768,
          'negative-control counts remain separate from 17304 audit records')

    # Deliberately altered serialized claims must fail the independent predicates.
    mutation_outcomes = {}
    obs = by_id[0]
    bad_log = obs['log_scaled_bounds']['l'][0][:]
    bad_log[0] += 2
    mutation_outcomes['lower_log_shifted_inward_by_two_units'] = not enclosure_is_valid(Q(obs['lower'][0]),bad_log)
    mutation_outcomes['duration_changed_by_one_reference_cycle'] = Q(obs['durations'][0])+1 != Q(obs['cycles'][0])*REFERENCE/Q(obs['multipliers'][0])
    duration = Q(obs['durations'][0])
    mutation_outcomes['rectangle_lower_increased_by_one'] = Q(obs['lower'][0])+1 != duration.numerator//duration.denominator-1
    admitted = next(r for r in reports if r['path']=='admit')
    altered = deepcopy(admitted)
    altered['certificate']['bias_scaled'][0] = 1
    mutation_outcomes['admitted_anchor_changed'] = bool(positive_errors(altered,by_id[altered['case_id']],report_claims(altered),delta[0]))
    altered = deepcopy(admitted)
    altered['certificate']['theta_scaled'][0] += 100*SCALE
    mutation_outcomes['admitted_original_variable_changed'] = bool(positive_errors(altered,by_id[altered['case_id']],report_claims(altered),delta[0]))
    rejected = next(r for r in reports if r['path']=='reject')
    altered = deepcopy(rejected)
    altered['certificate']['weights'][0] += 1
    altered['certificate']['total'] += 1
    mutation_outcomes['negative_edge_changed_but_sum_updated'] = bool(negative_errors(altered,graph_cache[altered['case_id']][1],report_claims(altered)))
    altered = deepcopy(rejected)
    altered['certificate']['total'] = 0
    mutation_outcomes['negative_cycle_sum_changed'] = bool(negative_errors(altered,graph_cache[altered['case_id']][1],report_claims(altered)))
    altered = deepcopy(admitted)
    altered['true'] = not altered['true']
    mutation_outcomes['truth_flag_flipped'] = altered['true'] != all(by_id[altered['case_id']]['cycles'][a] <= by_id[altered['case_id']]['cycles'][b] for a,b in report_claims(altered))
    altered = deepcopy(admitted)
    altered['beta_upper'] = str(Q(altered['beta_upper'])+1)
    mutation_outcomes['box_bound_changed'] = (Q(altered['beta_lower']),Q(altered['beta_upper'])) != all_anchor_beta(by_id[altered['case_id']],report_claims(altered))
    for name,detected in mutation_outcomes.items():
        check(detected,'mutation control detected: '+name)

    # Exact-boundary fixture: both true log endpoints are zero; outward uncertainty
    # creates an infeasible tightened graph but feasible relaxed graph. Abstain.
    boundary_obs = {'log_scaled_bounds':{'l':[[-1,1] for _ in range(6)],'u':[[-1,1] for _ in range(6)]}}
    boundary_status = classify(boundary_obs,FIXED,[0,0])
    check(boundary_status=='unknown','unresolved graph boundary explicitly returns unknown')
    box_boundary = box_class((Q(0),Q(2)),[1,1])
    check(box_boundary=='unknown','unresolved box boundary explicitly returns unknown')
    check(box_class((Q(1),Q(1)),[1,1])=='admit','box equality uses non-strict admission threshold')

    input_hashes = {name:sha(BASE/name) for name in ('PROTOCOL.json','OBSERVATIONS.json','RESULTS.json','ALL_REPORTS.jsonl.gz','SLOT_MAPPING_ADDENDUM.json')}
    for name in ('PROTOCOL.json','OBSERVATIONS.json','ALL_REPORTS.jsonl.gz'):
        check(input_hashes[name]==results['provenance'][name],'serialized input SHA256 '+name)
    out = {
        'status':'PASS' if not FAILURES else 'FAIL',
        'role':'Independent exact model/certificate validation; not a simulated scientific review',
        'scope':'Specified reset/settled/held digital-source model only. No RTL, silicon, GPU acquisition, physical bias calibration, timing, speedup, or workload prevalence validation.',
        'independence':{
            'producer_build_and_check_or_audit_core_read_imported_or_run':False,
            'prior_independent_checker_read':True,
            'arithmetic':'Python stdlib Fraction/integer, no Decimal, binary float or external numeric libraries',
            'logs':'130-term exact atanh series with geometric tail and power-of-two range reduction; every exact enclosure contained in the serialized 1e60 interval and narrower than 1e-100',
            'classification':'Independent Floyd-Warshall closure of relaxed and tightened 6-node difference graphs; certificates checked separately in original variables/edgewise',
            'source_hash_claims_in_RESULTS':'Producer source hashes are retained claims only; forbidden producer source files were not opened or independently hashed.',
        },
        'all_reports':normalized(all_counts),
        'total_orders':normalized(total_counts),
        'fixed_partials':normalized(partial_counts),
        'per_case_total_orders':{str(case):normalized(case_counts[case]) for case in range(24)},
        'checks':dict(COUNTS),
        'unique_rational_logarithms':log_interval.cache_info().currsize,
        'slot_mapping_clarification':{
            'prospective_protocol_repeated_mapping':False,
            'post_generation_addendum_checked':True,
            'prior_R03_protocol_mapping_checked':prior_mapping,
            'prior_R03_protocol_sha256':sha(prior_protocol_path),
            'serialized_fixed_clauses':FIXED,
            'effect':'Clarifies inherited index names only; does not change input evidence or prospectively preregister the clarification.',
        },
        'contract_negative_control':{'bad_edges':bad_edges,'reports':dict(contract_counts),'numerical_audits_performed':0,'population_separate_from_audit_stream':True},
        'negative_mutation_controls':mutation_outcomes,
        'unknown_boundary_controls':{'graph':boundary_status,'box':box_boundary,'actual_audit_stream_unknown':all_counts['unknown'],'actual_box_unknown':all_counts['box_unknown'],'minimum_actual_box_margin_scaled':str(min(boundary_distances))},
        'semantic_findings':[
            'All 144 legal adjacent edges including M0=10000 attain max(Mj/Mj-1,Mj-1/Mj)=201/200 exactly.',
            'Every duration and floor/ceil rectangle is checked separately for its own path; no rectangle is merged across paths.',
            'The original Ni determines truth. Equal Ni are retained as ties and all weakly true total and partial reports are admitted.',
            'An admitted false ranking establishes compatibility with some model witness, not truth of the original Ni ordering.',
            'For total orders beta uses all 15 transitive pairs; fixed partial uses the two retained index clauses.',
            'The new protocol names P<=F,A<=S but lists slots only numerically. The post-generation slot-mapping addendum is checked against the explicit prior R03 protocol; [[0,5],[4,1]] is checked in every serialized partial. This is a documentation repair, not prospective preregistration.',
            'No physical reset, fixed cycle count, settle/hold implementation, timer behavior, H20 observation, application cost or speedup is established.',
        ],
        'input_sha256':input_hashes,
        'validator_sha256':sha(Path(__file__)),
        'python':sys.version,
        'failures':FAILURES,
    }
    if not args.check_only:
        target = (HERE/args.output).resolve()
        if target.parent != HERE:
            raise ValueError('Output must remain in the independent directory')
        with target.open('x',encoding='utf-8') as stream:
            json.dump(out,stream,ensure_ascii=False,indent=2)
            stream.write('\n')
    print(json.dumps({'status':out['status'],'all_reports':out['all_reports'],'checks':out['checks'],
                      'control':out['contract_negative_control'],'mutations':mutation_outcomes,'failures':FAILURES},indent=2))
    return 0 if not FAILURES else 1


if __name__=='__main__':
    sys.exit(main())
