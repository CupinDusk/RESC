"""Independent author-side validation of the declared settled-clock construction.

This script reads serialized inputs and certificates. It neither imports, reads,
nor runs check_clock_contract.py. Only Python's standard library is used.
Run with bundled Python -B -X utf8. Writes only in this script's directory.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from pathlib import Path
import gzip
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SCALE = 10 ** 60
TERMS = 130
VECTORS = [
    [1000000, 1010000, 1006000, 998000, 1024000, 1002000],
    [1000000] * 6,
    [1000000, 1002000, 1004000, 1006000, 1008000, 1010000],
    [1010000, 1008000, 1006000, 1004000, 1002000, 1000000],
    [1000000, 1000500, 1001000, 1001500, 1002000, 1002500],
    [1000000, 1010000, 1020000, 1030000, 1040000, 1050000],
    [1002500, 1000000, 1002000, 1000500, 1001500, 1001000],
    [1024000, 1010000, 1006000, 998000, 1000000, 1002000],
]
PATHS = [[10000] * 6, [10001] * 6, [9999] * 6]
FIXED = [(0, 5), (4, 1)]
COUNTS = Counter()
FAILURES = []


def check(condition, label):
    COUNTS["assertions"] += 1
    if not condition:
        FAILURES.append(label)


def read_json(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def ratio_string(value):
    return f"{value.numerator}/{value.denominator}"


def atanh_enclosure(z):
    """For 0 <= z <= 1/3, exact partial sum and geometric upper tail."""
    assert Fraction(0) <= z <= Fraction(1, 3)
    power = z
    total = Fraction(0)
    zz = z * z
    for j in range(TERMS):
        total += power / (2 * j + 1)
        power *= zz
    lower = 2 * total
    remainder_bound = 2 * power / ((2 * TERMS + 1) * (1 - zz))
    return lower, lower + remainder_bound


LOG2 = atanh_enclosure(Fraction(1, 3))


@lru_cache(maxsize=None)
def log_enclosure(x):
    """Natural log using exact rational power-of-two range reduction."""
    assert x > 0
    k = 0
    r = x
    while r >= 2:
        r /= 2
        k += 1
    while r < 1:
        r *= 2
        k -= 1
    lower, upper = atanh_enclosure((r - 1) / (r + 1))
    if k >= 0:
        return lower + k * LOG2[0], upper + k * LOG2[1]
    return lower + k * LOG2[1], upper + k * LOG2[0]


def verify_log_bound(x, recorded, label):
    low, high = log_enclosure(x)
    check(Fraction(recorded[0], SCALE) <= low <= high <= Fraction(recorded[1], SCALE), label)
    check(high - low < Fraction(1, 10 ** 100), label + ": series enclosure width")
    check(recorded[0] <= recorded[1], label + ": ordered integer enclosure")
    COUNTS["exact_log_enclosures_verified"] += 1


def graph_bounds(obs, delta, tighten):
    """Eliminate shared biases: theta_j - theta_i <= u_j-l_i+|j-i|delta."""
    if tighten:
        lower = [x[1] for x in obs["log_scaled_bounds"]["l"]]
        upper = [x[0] for x in obs["log_scaled_bounds"]["u"]]
    else:
        lower = [x[0] for x in obs["log_scaled_bounds"]["l"]]
        upper = [x[1] for x in obs["log_scaled_bounds"]["u"]]
    return [[upper[j] - lower[i] + abs(j - i) * delta
             for j in range(6)] for i in range(6)]


def has_negative_cycle(pair_weights, claims):
    """Fresh all-pairs shortest-path closure, no original auditor code."""
    matrix = [row[:] for row in pair_weights]
    for i in range(6):
        matrix[i][i] = min(matrix[i][i], 0)
    for smaller, larger in claims:
        # theta_smaller <= theta_larger is larger -> smaller, weight zero.
        matrix[larger][smaller] = min(matrix[larger][smaller], 0)
    for middle in range(6):
        for start in range(6):
            for end in range(6):
                matrix[start][end] = min(
                    matrix[start][end],
                    matrix[start][middle] + matrix[middle][end])
    COUNTS["independent_floyd_closures"] += 1
    return any(matrix[i][i] < 0 for i in range(6))


def all_pairs_of_order(order):
    return [(a, b) for index, a in enumerate(order) for b in order[index + 1:]]


def report_beta(obs, claims):
    """Supremum over EVERY real anchor, retaining the report's rank closure."""
    low = obs["log_scaled_bounds"]["l"]
    high = obs["log_scaled_bounds"]["u"]
    beta_lower = max([Fraction(0)] + [
        Fraction(low[a][0] - high[b][1], abs(a - b)) for a, b in claims])
    beta_upper = max([Fraction(0)] + [
        Fraction(low[a][1] - high[b][0], abs(a - b)) for a, b in claims])
    return beta_lower, beta_upper


def verify_positive_certificate(report, obs, claims, delta):
    certificate = report["certificate"]
    theta = certificate["theta_scaled"]
    bias = certificate["bias_scaled"]
    label = f"case {report['case_id']} {report['kind']} {report.get('order', '')}"
    check(len(theta) == 6 and len(bias) == 7, label + ": witness dimensions")
    check(all(type(x) is int for x in theta + bias), label + ": integer witness")
    check(bias[0] == 0, label + ": anchor")
    for i in range(6):
        value = theta[i] + bias[i + 1]
        check(obs["log_scaled_bounds"]["l"][i][1] <= value <=
              obs["log_scaled_bounds"]["u"][i][0], label + f": tightened rectangle {i}")
        check(abs(bias[i + 1] - bias[i]) <= delta, label + f": Lipschitz edge {i}")
        COUNTS["positive_witness_rectangle_checks"] += 1
        COUNTS["positive_witness_lipschitz_checks"] += 1
    for a, b in claims:
        check(theta[a] <= theta[b], label + f": rank {a}<={b}")
        COUNTS["positive_witness_rank_checks"] += 1
    COUNTS["positive_original_variable_certificates"] += 1


def verify_negative_certificate(report, relaxed, claims):
    certificate = report["certificate"]
    cycle = certificate["cycle"]
    weights = certificate["weights"]
    label = f"case {report['case_id']} {report['kind']} {report.get('order', '')}"
    check(len(cycle) == len(weights) and len(cycle) > 0, label + ": cycle length")
    rank_edges = {(b, a) for a, b in claims}
    for k, ((start, end), weight) in enumerate(zip(cycle, weights)):
        check(end == cycle[(k + 1) % len(cycle)][0], label + ": cycle continuity")
        valid_pair = weight == relaxed[start][end]
        valid_rank = (start, end) in rank_edges and weight == 0
        check(valid_pair or valid_rank, label + f": certified edge {start}->{end}")
        COUNTS["negative_cycle_edges_verified"] += 1
        if valid_rank:
            COUNTS["negative_cycle_ranking_edges_verified"] += 1
    check(sum(weights) == certificate["total"] < 0, label + ": strictly negative sum")
    COUNTS["negative_cycle_certificates"] += 1


def main():
    protocol = read_json("PROTOCOL.json")
    numeric = read_json("NUMERIC_PROTOCOL_ADDENDUM.json")
    observations = read_json("OBSERVATIONS.json")
    results = read_json("RESULTS.json")
    with gzip.open(BASE / "ALL_REPORTS.jsonl.gz", "rt", encoding="utf-8") as stream:
        reports = [json.loads(line) for line in stream if line.strip()]

    check(protocol["cycle_count_vectors_in_slot_order"] == VECTORS, "predeclared cycle vectors")
    check(protocol["three_replay_multiplier_sequences"] == PATHS, "predeclared multiplier paths")
    check(protocol["slots"] == dict(zip("PSBGAF", range(1, 7))), "slot order")
    check(protocol["clock_contract"]["reference_multiplier"] == 10000, "reference multiplier")
    check(int(results["scale"]) == SCALE, "integer unit scale")
    check(len(observations) == 8, "all eight observations")
    check(len(reports) == 5768, "all 5760 total orders and eight partial reports")
    delta_bounds = results["delta_scaled_enclosure"]
    verify_log_bound(Fraction(1005, 1000), delta_bounds, "guard log enclosure")

    # Each numerator is literally advanced once per fixed job cycle. Dividing
    # by the held multiplier only after accumulation avoids timing/float code.
    for case, obs in enumerate(observations):
        check(obs["case_id"] == case and obs["cycles"] == VECTORS[case], f"case {case}: identity")
        check(obs["multipliers"] == PATHS, f"case {case}: paths")
        independent_times = []
        for path_id, path in enumerate(PATHS):
            previous = 10000
            replay = []
            for arm, (cycles, multiplier) in enumerate(zip(VECTORS[case], path)):
                check(1000 * multiplier <= 1005 * previous and
                      1000 * previous <= 1005 * multiplier,
                      f"case {case} replay {path_id} arm {arm}: reciprocal guard")
                previous = multiplier
                COUNTS["exact_controller_boundary_checks"] += 1
                accumulated_numerator = 0
                for unused_cycle in range(cycles):
                    accumulated_numerator += 10000
                value = Fraction(accumulated_numerator, multiplier)
                replay.append(value)
                check(value == Fraction(obs["normalized_durations"][path_id][arm]),
                      f"case {case} replay {path_id} arm {arm}: literal rational duration")
                COUNTS["literal_cycle_increments"] += cycles
                COUNTS["rational_observations_verified"] += 1
            independent_times.append(replay)
        for arm in range(6):
            lower = min(row[arm] for row in independent_times)
            upper = max(row[arm] for row in independent_times)
            check(lower == Fraction(obs["lower"][arm]) and upper == Fraction(obs["upper"][arm]),
                  f"case {case} arm {arm}: exact min/max rectangle")
            check(0 < lower < upper, f"case {case} arm {arm}: positive-width positive rectangle")
            verify_log_bound(lower, obs["log_scaled_bounds"]["l"][arm], f"case {case} arm {arm}: lower log")
            verify_log_bound(upper, obs["log_scaled_bounds"]["u"][arm], f"case {case} arm {arm}: upper log")
            # ln N + ln(10000/M) = ln T exactly: no floating truth estimate.
            for path_id, path in enumerate(PATHS):
                check(Fraction(VECTORS[case][arm]) * Fraction(10000, path[arm]) ==
                      independent_times[path_id][arm], f"case {case}: exact multiplicative model identity")
                check(lower <= independent_times[path_id][arm] <= upper,
                      f"case {case}: original truth and replay in rectangle")
                COUNTS["original_truth_replay_rectangle_checks"] += 1
        COUNTS["positive_width_rectangles"] += 6

    expected_total_ids = {(case, order) for case in range(8) for order in permutations(range(6))}
    seen_total_ids = set()
    seen_partial_ids = set()
    overall = Counter()
    total_orders = Counter()
    partials = Counter()
    by_case = [Counter() for unused in range(8)]
    box_counts = Counter()
    graph_cache = {}
    for case, obs in enumerate(observations):
        graph_cache[case] = (
            graph_bounds(obs, delta_bounds[0], True),
            graph_bounds(obs, delta_bounds[1], False))
    partial_records = []
    for report in reports:
        case = report["case_id"]
        obs = observations[case]
        if report["kind"] == "total_order":
            order = tuple(report["order"])
            check((case, order) not in seen_total_ids, "duplicate total order")
            seen_total_ids.add((case, order))
            claims = all_pairs_of_order(order)
            bucket = total_orders
        else:
            check(report["kind"] == "fixed_partial", "declared report kind")
            check(case not in seen_partial_ids, "duplicate fixed partial")
            seen_partial_ids.add(case)
            claims = [tuple(pair) for pair in report["claims"]]
            check(claims == FIXED, "fixed partial clauses")
            bucket = partials
            partial_records.append(report)
        truth = all(VECTORS[case][a] <= VECTORS[case][b] for a, b in claims)
        check(report["true"] == truth, "truth independently from integer cycle counts")
        tightened, relaxed = graph_cache[case]
        relaxed_infeasible = has_negative_cycle(relaxed, claims)
        tightened_infeasible = has_negative_cycle(tightened, claims)
        status = "reject" if relaxed_infeasible else "admit" if not tightened_infeasible else "unknown"
        check(status == report["path"], "independent graph classification")
        if report["path"] == "admit":
            verify_positive_certificate(report, obs, claims, delta_bounds[0])
        elif report["path"] == "reject":
            verify_negative_certificate(report, relaxed, claims)
        else:
            check(report["path"] == "unknown", "unknown retained")
        beta_lower, beta_upper = report_beta(obs, claims)
        check(beta_lower == Fraction(report["beta_lower"]) and
              beta_upper == Fraction(report["beta_upper"]), "independent all-real-anchor beta enclosure")
        box = "admit" if beta_upper <= delta_bounds[0] else "reject" if beta_lower > delta_bounds[1] else "unknown"
        check(box == report["box"], "independent all-real-anchor box classification")
        box_counts[box] += 1
        for count in (overall, bucket, by_case[case]):
            count["reports"] += 1
            count[status] += 1
            count["true_reports"] += truth
            count["true_admitted"] += truth and status == "admit"
            count["true_rejected"] += truth and status == "reject"
            count["incorrect_but_admitted"] += not truth and status == "admit"
            count["boxes_admit_path_reject"] += box == "admit" and status == "reject"
        if report["kind"] == "total_order":
            by_case[case]["orders"] += 1
        COUNTS["report_truth_checks"] += 1
        COUNTS["anchor_beta_enclosures_verified"] += 1
    check(seen_total_ids == expected_total_ids, "complete exact 8*720 total-order enumeration")
    check(seen_partial_ids == set(range(8)), "all eight fixed partials")
    check(sorted(partial_records, key=lambda r: r["case_id"]) == results["fixed_partial"], "RESULTS partial records identical")
    for case, obs in enumerate(observations):
        check(obs["fixed_partial"] in partial_records, f"case {case}: observation partial cross-reference")
        for key, recorded in obs["total_order_summary"].items():
            if key == "orders":
                actual = 720
            else:
                # by_case contains one partial as well; remove its contribution.
                partial = obs["fixed_partial"]
                contribution = {
                    "admit": partial["path"] == "admit",
                    "reject": partial["path"] == "reject",
                    "unknown": partial["path"] == "unknown",
                    "true_reports": partial["true"],
                    "incorrect_but_admitted": not partial["true"] and partial["path"] == "admit",
                    "boxes_admit_path_reject": partial["box"] == "admit" and partial["path"] == "reject",
                }[key]
                actual = by_case[case][key] - contribution
            check(actual == recorded, f"case {case}: summary {key}")
    for key, recorded in results["total_order_summary"].items():
        actual = total_orders["reports"] if key == "orders" else total_orders[key]
        check(actual == recorded, f"RESULTS total-order summary {key}")
    check(results["controller_boundary_checks"] == COUNTS["exact_controller_boundary_checks"], "RESULTS controller count")
    check(results["job_vectors"] == 8 and results["replays"] == 24, "RESULTS vector/replay counts")
    check(results["graph_bf_and_independent_floyd_checks"] == COUNTS["independent_floyd_closures"], "RESULTS graph count")
    check(results["original_variable_admission_certificates"] == COUNTS["positive_original_variable_certificates"], "RESULTS positive certificate count")
    check(results["negative_cycle_certificates"] == COUNTS["negative_cycle_certificates"], "RESULTS negative certificate count")
    check(results["unknown"] == overall["unknown"], "RESULTS unknown count")

    # Case 0: F->P and S->A are rank edges; P->S and A->F
    # are one-boundary observation edges. Its sum is 2 delta+uS-lP+uF-lA.
    first = observations[0]["log_scaled_bounds"]
    threshold_lower = Fraction(first["l"][0][0] + first["l"][4][0] - first["u"][1][1] - first["u"][5][1], 2)
    threshold_upper = Fraction(first["l"][0][1] + first["l"][4][1] - first["u"][1][0] - first["u"][5][0], 2)
    beta_lower, beta_upper = report_beta(observations[0], FIXED)
    check(beta_upper <= delta_bounds[0] < delta_bounds[1] < threshold_lower,
          "case 0 rigorous beta <= guard < four-arm cycle threshold")

    inputs = {}
    for name in ("PROTOCOL.json", "NUMERIC_PROTOCOL_ADDENDUM.json", "OBSERVATIONS.json", "RESULTS.json", "ALL_REPORTS.jsonl.gz"):
        inputs[name] = hashlib.sha256((BASE / name).read_bytes()).hexdigest()
    for name in ("PROTOCOL.json", "NUMERIC_PROTOCOL_ADDENDUM.json", "ALL_REPORTS.jsonl.gz"):
        check(inputs[name] == results["provenance"][name], f"RESULTS provenance {name}")
    for bucket in (overall, total_orders, partials, box_counts):
        for status in ("admit", "reject", "unknown"):
            bucket[status] += 0
    output = {
        "status": "PASS" if not FAILURES else "FAIL",
        "role": "Independent author-side model/certificate validation, not a paper review",
        "scope": "Declared digital settled-clock, fixed-cycle model only; no physical measurements or GPU validation",
        "independence": {
            "original_auditor_imported_read_or_executed": False,
            "arithmetic": "stdlib Fraction and integer only; no Decimal/mpmath/floating point",
            "logarithm_proof": "130-term exact rational atanh series after power-of-two reduction, including exact geometric upper tail; cached exact ln(2) interval",
            "numerical_enclosure_guarantee": "Each independent exact rational log enclosure is contained in the recorded scaled integer interval, and has width below 1e-100",
            "acquisition_check": "Literal per-cycle numerator accumulation followed by one exact Fraction division, for every modeled job/replay",
            "graph_check": "Fresh six-node all-pairs shortest-path closure on tightened and relaxed edge bounds; serialized certificates verified separately edgewise",
        },
        "all_reports": dict(overall),
        "total_orders": dict(total_orders),
        "fixed_partials": dict(partials),
        "all_real_anchor_box_statuses": dict(box_counts),
        "checks": dict(COUNTS),
        "unique_rational_logarithms": log_enclosure.cache_info().currsize,
        "worked_case_0_scaled_enclosures": {
            "scale": str(SCALE),
            "beta_R": [ratio_string(beta_lower), ratio_string(beta_upper)],
            "guard_delta": [str(value) for value in delta_bounds],
            "four_arm_cycle_threshold": [ratio_string(threshold_lower), ratio_string(threshold_upper)],
            "cycle_formula": "2*delta+u_S-l_P+u_F-l_A",
            "negative_cycle_relaxed_sum": results["fixed_partial"][0]["certificate"]["total"],
            "all_anchor_boxes_admit_and_common_path_rejects": True,
        },
        "semantic_findings": [
            "The model identity follows algebraically from fixed reset cycle counts and a settled multiplier held throughout each command; these are assumptions, not hardware observations.",
            "The box baseline quantifies every real anchor separately; its witness may depend on anchor. It does not assert one common path or one witness shared across anchors.",
            "Total orders use all 15 transitive ranking pairs in beta_R; retaining only five adjacent clauses would weaken the baseline.",
            "All replay paths are constant after the reference-to-first boundary. They obey but do not stress or establish tightness of the guard.",
            "All six per-arm rectangle extrema come from the same two constant paths in this construction, so rectangles are an explicit abstraction rather than measured noise distributions.",
            "Incorrect-but-admitted reports remain possible: admission certifies model compatibility, not truth of the original cycle-count ordering.",
            "No inference about GPU clock settling, fixed cycle counts, same-state semantics, execution cost, H20 observations, prevalence, or physical drift is licensed.",
        ],
        "failures": FAILURES,
        "input_sha256": inputs,
        "validator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version,
    }
    (HERE / "VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "all_reports": output["all_reports"], "checks": output["checks"], "failures": FAILURES}, indent=2))
    return not FAILURES


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
