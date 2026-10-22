"""Prespecified complete-all-slot sharpness checks, exact witnesses + LPs."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import hashlib, json
from hopper_explanation_radius import min_lp, feasibility
from hopper_partial_orders import box_min_lp

HERE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = HERE / 'HOPPER_R10_FULL_ORDER_RESULTS.json'
    assert not out.exists()
    records, path_min_count, box_min_count, feasible_count = [], 0, 0, 0
    max_path_error = max_box_error = max_witness_violation = 0.
    for N in [4, 5, 6, 8, 16, 32, 64]:
        for eps in [Fraction(0), Fraction(1, 1000), Fraction(4, 1000)]:
            t = Fraction(1, 100)
            v = t - 2*eps
            beta = v / (N-2)
            c = {1: t, 2: v-beta, N-1: Fraction(0), N: t+v-beta}
            c.update({j: v-beta*(j-1) for j in range(3, N-1)})
            assert len(c) == N
            order = [1, N-1] + list(range(N-2, 2, -1)) + [N, 2]
            assert sorted(order) == list(range(1, N+1))
            allpairs = list(combinations(order, 2))
            chain = list(zip(order, order[1:]))
            lq = {j: c[j]-eps for j in range(1, N+1)}
            uq = {j: c[j]+eps for j in range(1, N+1)}
            thresholds = [max(Fraction(0), (lq[p]-uq[q])/abs(p-q)) for p, q in allpairs]
            assert max(thresholds) == beta
            # Exact original x/b witness, including the floor at slot zero.
            bq = {j: (-v if 2 <= j <= N-1 else Fraction(0)) for j in range(N+1)}
            xq = {j: (lq[j] if j in [1, N] else uq[j]) for j in range(1, N+1)}
            tq = {j: xq[j]-bq[j] for j in range(1, N+1)}
            assert all(lq[j] <= xq[j] <= uq[j] for j in xq)
            assert bq[0] == 0 and max(abs(bq[j]-bq[j-1]) for j in range(1, N+1)) == v
            assert all(tq[p] <= tq[q] for p, q in allpairs)
            assert (lq[1]-uq[N-1] + lq[N]-uq[2])/2 == v
            l, u = {j: float(lq[j]) for j in lq}, {j: float(uq[j]) for j in uq}
            pos = {j: j for j in lq}
            optimum, witness = min_lp(l, u, pos, chain)
            path_min_count += 1
            err = abs(optimum-float(v))
            max_path_error = max(max_path_error, err)
            max_witness_violation = max(max_witness_violation, witness['maximum_ranking_violation'])
            assert err <= 1e-8 and witness['maximum_ranking_violation'] <= 1e-8
            anchors = [Fraction(j, 2) for j in range(2*N+1)] + [Fraction(N+1)]
            anchored = []
            for anchor in anchors:
                analytic = max([Fraction(0)] + [(lq[p]-uq[q])/(abs(p-anchor)+abs(q-anchor)) for p, q in allpairs])
                actual = box_min_lp(l, u, pos, chain, float(anchor))
                box_min_count += 1
                max_box_error = max(max_box_error, abs(actual-float(analytic)))
                assert abs(actual-float(analytic)) <= 1e-8
                anchored.append({'anchor': str(anchor), 'analytic_radius': str(analytic), 'original_box_LP_radius': actual})
            assert max(Fraction(r['analytic_radius']) for r in anchored) == beta
            samples = []
            for delta in [Fraction(99, 100)*beta, beta, (beta+v)/2, Fraction(999, 1000)*v, v, Fraction(1001, 1000)*v]:
                path = feasibility(l, u, pos, chain, float(delta))
                feasible_count += 1
                assert path == (delta >= v)
                boxes = []
                for anchor in anchors:
                    admitted = feasibility(l, u, pos, chain, float(delta), float(anchor))
                    feasible_count += 1
                    expected = delta >= Fraction(anchored[len(boxes)]['analytic_radius'])
                    assert admitted == expected, (N, eps, delta, anchor, admitted, expected)
                    boxes.append(admitted)
                assert all(boxes) == (delta >= beta)
                samples.append({'delta': str(delta), 'shared_path_feasible': path, 'all_anchor_boxes_feasible': all(boxes), 'box_feasibility_by_anchor': boxes})
            records.append({'N': N, 't': str(t), 'epsilon': str(eps), 'v': str(v), 'all_anchor_radius': str(beta), 'shared_radius': str(v), 'ratio': N-2, 'complete_order': order, 'centers': {str(j): str(c[j]) for j in c}, 'explicit_x': {str(j): str(xq[j]) for j in xq}, 'explicit_bias': {str(j): str(bq[j]) for j in bq}, 'explicit_theta': {str(j): str(tq[j]) for j in tq}, 'all_implied_comparisons': len(allpairs), 'original_path_LP_radius': optimum, 'anchored_minima': anchored, 'samples': samples})
        print(json.dumps({'stage': 'full_order_sharpness', 'N': N, 'cases': len(records), 'path_min_LPs': path_min_count, 'box_min_LPs': box_min_count, 'feasibility_LPs': feasible_count}), flush=True)
    result = {'result': 'PASS_N_MINUS_2_SHARP_FOR_COMPLETE_ORDER_OF_ALL_N_SLOTS', 'protocol_sha256': sha(HERE/'HOPPER_R10_CERTIFICATION_PROTOCOL.json'), 'argument_sha256': sha(HERE/'HOPPER_R10_TOTAL_ORDER_ARGUMENT_DRAFT.md'), 'script_sha256': sha(Path(__file__)), 'cases': len(records), 'path_minimum_LPs': path_min_count, 'box_minimum_LPs': box_min_count, 'feasibility_LPs': feasible_count, 'maximum_path_radius_error': max_path_error, 'maximum_box_radius_error': max_box_error, 'maximum_attaining_path_ranking_violation': max_witness_violation, 'records': records, 'scope': 'Controlled log rectangles and exact rational analytic witnesses; original x/b LP cross-checks use SciPy HiGHS feasibility tolerance1e-9 and comparison tolerance1e-8. No new hardware data or physical error calibration.'}
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, indent=2), flush=True)

if __name__ == '__main__':
    main()
