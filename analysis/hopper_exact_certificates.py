"""Outward log intervals followed by exact integer difference constraints.

This certifies conditional arithmetic for exact decimal timing endpoints. It
does not calibrate a physical bias budget or validate native acquisition.
"""
from pathlib import Path
from itertools import combinations, permutations
from collections import defaultdict, Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import argparse, csv, hashlib, json

HERE = Path(__file__).resolve().parent
MATRIX = HERE.parent / 'artifacts/hopper-retained-v1/selected-summary-matrix.csv'
ARMS = ['PULL', 'PULL_FLAT', 'PUSH_ST', 'GLOBAL', 'PUSH_BULK', 'PUSH_STASYNC']
POS = [1, 6, 2, 4, 3, 5]
U = 60 * 10**60
ETA = U // 10**8
GRID = ['0', '.005', '.01', '.02', '.05', '.10']
CERT = HERE / 'HOPPER_R10_EXACT_CERTIFICATES.jsonl'
RESULT = HERE / 'HOPPER_R10_EXACT_RESULTS.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def log_bounds(value):
    x = Decimal(value)
    assert x > 0
    if x == 1:
        return 0, 0
    with localcontext() as ctx:
        ctx.prec = 80
        v = x.ln()
        low, high = v.next_minus(), v.next_plus()
    with localcontext() as ctx:
        ctx.prec = 110
        a = int((low * 10**60).to_integral_value(rounding=ROUND_FLOOR)) * 60
        b = int((high * 10**60).to_integral_value(rounding=ROUND_CEILING)) * 60
    assert a <= b
    return a, b

def load_cells():
    cells = defaultdict(dict)
    with MATRIX.open(encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            key = (r['pattern'], int(r['C']), int(r['launched_clusters']), int(r['payload_B']))
            cells[key][r['arm']] = (r['min_ns'], r['max_ns'])
    out = []
    for key, rows in sorted(cells.items()):
        low = [log_bounds(rows[a][0]) for a in ARMS]
        high = [log_bounds(rows[a][1]) for a in ARMS]
        assert all(Decimal(rows[a][0]) <= Decimal(rows[a][1]) for a in ARMS)
        out.append((key, low, high))
    assert len(out) == 89
    return out

def beta_bounds(low, high, comparisons):
    lo = hi = 0
    for p, q in comparisons:
        d = abs(POS[p] - POS[q])
        nlo = low[p][0] - high[q][1]
        nhi = low[p][1] - high[q][0]
        assert nlo % d == nhi % d == 0
        lo = max(lo, nlo // d)
        hi = max(hi, nhi // d)
    assert lo <= hi
    return lo, hi

def graph(low, high, comparisons, delta, relaxed):
    # tuple: from, to, weight, constant, distance, kind
    edges = []
    for a in range(6):
        for b in range(6):
            if a == b:
                continue
            c = high[b][1 if relaxed else 0] - low[a][0 if relaxed else 1]
            d = abs(POS[a] - POS[b])
            edges.append((a, b, c + delta*d, c, d, 'observation'))
    edges.extend((q, p, 0, 0, 0, 'ranking') for p, q in comparisons)
    return edges

def exact_feasibility(edges):
    dist = [0] * 6
    pred = [None] * 6
    for _ in range(6):
        changed = None
        for e in edges:
            a, b, w = e[:3]
            if dist[b] > dist[a] + w:
                dist[b] = dist[a] + w
                pred[b] = e
                changed = b
        if changed is None:
            assert all(dist[b] - dist[a] <= w for a, b, w, *_ in edges)
            return {'potential': dist}
    v = changed
    for _ in range(6):
        assert pred[v] is not None
        v = pred[v][0]
    start, backward = v, []
    while True:
        e = pred[v]
        backward.append(e)
        v = e[0]
        if v == start:
            break
        assert len(backward) <= 6
    cycle = list(reversed(backward))
    assert all(cycle[i][1] == cycle[(i+1) % len(cycle)][0] for i in range(len(cycle)))
    assert sum(e[2] for e in cycle) < 0
    return {'cycle': cycle}

def certify(low, high, comparisons, blo, bhi, try_positive):
    def positive():
        budget = bhi + ETA
        ans = exact_feasibility(graph(low, high, comparisons, budget, True))
        if 'cycle' not in ans:
            return None
        cycle = ans['cycle']
        c, d = sum(e[3] for e in cycle), sum(e[4] for e in cycle)
        assert d > 0
        bound = Fraction(-c - bhi*d, d*U)
        assert bound > Fraction(1, 10**8)
        return {'classification': 'width_gt_eta', 'budget': str(budget),
                'cycle': [[e[0], e[1], str(e[2]), e[5]] for e in cycle],
                'cycle_sum': str(sum(e[2] for e in cycle)),
                'width_lower_bound': [str(bound.numerator), str(bound.denominator)]}
    def nonpositive():
        budget = blo + ETA
        ans = exact_feasibility(graph(low, high, comparisons, budget, False))
        if 'potential' not in ans:
            return None
        return {'classification': 'width_le_eta', 'budget': str(budget),
                'potential': [str(v) for v in ans['potential']]}
    for fn in ([positive, nonpositive] if try_positive else [nonpositive, positive]):
        ans = fn()
        if ans is not None:
            return ans
    return {'classification': 'ambiguous'}

def verify_record(rec, low, high, comparisons, blo, bhi):
    assert int(rec['beta_lower']) == blo and int(rec['beta_upper']) == bhi
    kind = rec['classification']
    if kind == 'width_gt_eta':
        delta = int(rec['budget'])
        assert delta == bhi + ETA
        allowed = {(a, b, k): (w, c, d) for a, b, w, c, d, k in graph(low, high, comparisons, delta, True)}
        cycle = rec['cycle']
        assert cycle and all(cycle[i][1] == cycle[(i+1) % len(cycle)][0] for i in range(len(cycle)))
        csum = dsum = wsum = 0
        for a, b, w, k in cycle:
            exact, c, d = allowed[(a, b, k)]
            assert int(w) == exact
            csum += c
            dsum += d
            wsum += exact
        assert wsum < 0 and str(wsum) == rec['cycle_sum'] and dsum > 0
        lower = Fraction(-csum - bhi*dsum, dsum*U)
        assert lower > Fraction(1, 10**8)
        assert lower == Fraction(*map(int, rec['width_lower_bound']))
        return lower
    if kind == 'width_le_eta':
        delta = int(rec['budget'])
        assert delta == blo + ETA
        potential = list(map(int, rec['potential']))
        assert len(potential) == 6
        assert all(potential[b] - potential[a] <= w for a, b, w, *_ in graph(low, high, comparisons, delta, False))
        return None
    assert kind == 'ambiguous'
    return None

def fixed_order(low, high, comparisons, blo, bhi, dlo, dhi):
    if blo > dhi:
        return 'no_gap_box_rejects'
    if 'potential' in exact_feasibility(graph(low, high, comparisons, dlo, False)):
        return 'no_gap_path_admits'
    if bhi <= dlo and 'cycle' in exact_feasibility(graph(low, high, comparisons, dhi, True)):
        return 'gap'
    return 'ambiguous'

def fixed_two(low, high, query, dlo, dhi):
    p, q, r, s = query
    def margin(a, b):
        d = abs(POS[a] - POS[b])
        return high[b][0] - low[a][1] + dlo*d, high[b][1] - low[a][0] + dhi*d
    a, b = margin(p, q), margin(r, s)
    cx1, cx2 = margin(p, s), margin(r, q)
    cx = (cx1[0] + cx2[0], cx1[1] + cx2[1])
    if a[0] >= 0 and b[0] >= 0 and cx[1] < 0:
        return 'gap'
    if a[1] < 0 or b[1] < 0 or cx[0] >= 0:
        return 'no_gap'
    return 'ambiguous'

def verify_file():
    cells = load_cells()
    orders = list(permutations(sorted(range(6), key=lambda j: ARMS[j])))
    counts, total = Counter(), 0
    with CERT.open(encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            cell_index, order_index = divmod(total, 720)
            key, low, high = cells[cell_index]
            order = orders[order_index]
            assert r['case'] == total and r['cell'] == list(key) and r['order'] == [ARMS[a] for a in order]
            pairs = list(combinations(order, 2))
            blo, bhi = beta_bounds(low, high, pairs)
            verify_record(r, low, high, pairs, blo, bhi)
            counts[r['classification']] += 1
            total += 1
    assert total == 64080
    result = json.loads(RESULT.read_text(encoding='utf-8'))
    assert sha(CERT) == result['certificate_sha256']
    assert dict(counts) == result['classification_counts']
    print(json.dumps({'result': 'PASS_REPLAY_ALL_EXACT_CERTIFICATES', 'cases': total, 'counts': counts, 'certificate_sha256': sha(CERT)}), flush=True)

def main():
    assert not CERT.exists() and not RESULT.exists()
    cells = load_cells()
    orders = list(permutations(sorted(range(6), key=lambda j: ARMS[j])))
    budget_bounds = {f: log_bounds(str(Decimal(1) + Decimal(f))) for f in GRID}
    oldcsv = HERE / 'HOPPER_R9_ALL_TOTAL_ORDERS.csv'
    oldrows = list(csv.DictReader(oldcsv.open(encoding='utf-8', newline='')))
    assert len(oldrows) == 64080
    widths = [float(r['window_width']) for r in oldrows]
    counts, total, smallest_bound, positive_cells = Counter(), 0, None, set()
    fixed = {f: {'states': Counter(), 'cells': set()} for f in GRID}
    twos = {f: {'states': Counter(), 'cells': set()} for f in GRID}
    queries = sorted(q for q in permutations(range(6), 4) if tuple(ARMS[a] for a in q[:2]) < tuple(ARMS[a] for a in q[2:]))
    assert len(queries) == 180
    with CERT.open('w', encoding='utf-8', newline='\n') as fout:
        for ci, (key, low, high) in enumerate(cells):
            for order in orders:
                old = oldrows[total]
                assert (old['pattern'], int(old['C']), int(old['clusters']), int(old['payload_B'])) == key
                assert old['order'] == '<='.join(ARMS[j] for j in order)
                pairs = list(combinations(order, 2))
                blo, bhi = beta_bounds(low, high, pairs)
                r = {'case': total, 'cell': key, 'order': [ARMS[j] for j in order],
                     'beta_lower': str(blo), 'beta_upper': str(bhi),
                     **certify(low, high, pairs, blo, bhi, widths[total] > 1e-8)}
                bound = verify_record(r, low, high, pairs, blo, bhi)
                if bound is not None:
                    smallest_bound = bound if smallest_bound is None else min(smallest_bound, bound)
                    positive_cells.add(key)
                counts[r['classification']] += 1
                fout.write(json.dumps(r, separators=(',', ':')) + '\n')
                for f, (dlo, dhi) in budget_bounds.items():
                    state = 'no_gap_zero_bias' if f == '0' else fixed_order(low, high, pairs, blo, bhi, dlo, dhi)
                    fixed[f]['states'][state] += 1
                    if state == 'gap':
                        fixed[f]['cells'].add(key)
                total += 1
            for query in queries:
                for f, (dlo, dhi) in budget_bounds.items():
                    state = 'no_gap_zero_bias' if f == '0' else fixed_two(low, high, query, dlo, dhi)
                    twos[f]['states'][state] += 1
                    if state == 'gap':
                        twos[f]['cells'].add(key)
            if (ci+1) % 8 == 0 or ci == 88:
                print(json.dumps({'stage': 'exact_certification', 'cells': ci+1, 'orders': total, 'counts': counts}), flush=True)
    def tabulate(data):
        return [{'fraction': f, 'states': dict(v['states']), 'gap_queries': v['states']['gap'], 'distinct_gap_cells': len(v['cells']), 'gap_cell_identities': sorted(v['cells'])} for f, v in data.items()]
    positive_widths = [v for v in widths if v > 1e-10]
    result = {'result': 'PASS_EXACT_RESOLUTION_PARTITION' if counts['ambiguous'] == 0 else 'PARTIAL_CERTIFICATION_WITH_AMBIGUOUS_CASES',
              'eta_log_budget_units': '1e-8', 'integer_scale': str(U), 'log_precision_digits': 80,
              'log_grid': '1e-60', 'decimal_rounding_contract': 'Python3.12 Decimal.ln correctly rounded ROUND_HALF_EVEN; adjacent values then outward integer grid',
              'matrix_sha256': sha(MATRIX), 'protocol_sha256': sha(HERE / 'HOPPER_R10_CERTIFICATION_PROTOCOL.json'),
              'argument_sha256': sha(HERE / 'HOPPER_R10_CERTIFICATION_ARGUMENT.md'), 'script_sha256': sha(Path(__file__)),
              'historical_numeric_csv_sha256': sha(oldcsv), 'total_orders': total, 'distinct_cells': len(cells),
              'classification_counts': dict(counts), 'positive_window_cells': len(positive_cells),
              'minimum_certified_positive_width_lower_bound': [str(smallest_bound.numerator), str(smallest_bound.denominator)] if smallest_bound is not None else None,
              'minimum_certified_positive_width_lower_bound_approx': float(smallest_bound) if smallest_bound is not None else None,
              'historical_numeric_width_sensitivity_only': [{'threshold': v, 'counts_above': sum(w > v for w in widths)} for v in [1e-12, 1e-10, 1e-9, 1e-8]],
              'historical_minimum_width_above_1e-10': min(positive_widths),
              'fixed_budget_total_orders': tabulate(fixed), 'fixed_budget_two_disjoint_claims': tabulate(twos),
              'certificate_sha256': sha(CERT), 'certificate_bytes': CERT.stat().st_size,
              'scope': 'No LP solver is used by certification or replay. Every certificate is checked edgewise with exact integers. This is conditional arithmetic for the declared rectangles and log-bias model, not a physical timing bound, hardware validation or proof of Decimal internals.'}
    RESULT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if not k.startswith('fixed_budget')}, indent=2), flush=True)
    print(json.dumps({'fixed_orders': [(r['fraction'], r['gap_queries'], r['distinct_gap_cells'], r['states'].get('ambiguous', 0)) for r in result['fixed_budget_total_orders']], 'fixed_pairs': [(r['fraction'], r['gap_queries'], r['distinct_gap_cells'], r['states'].get('ambiguous', 0)) for r in result['fixed_budget_two_disjoint_claims']]}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-certificates', action='store_true')
    args = parser.parse_args()
    verify_file() if args.verify_certificates else main()
