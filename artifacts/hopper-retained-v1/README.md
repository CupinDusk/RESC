# Retained H20 numerical reanalysis, version 1

This local author artifact contains existing measurement summaries, not new GPU results. It has not been publicly archived. It requires no account, original repository, compiler, network access or historical launcher.

Run from this directory using Python 3.12 with NumPy:

```text
python -B -X utf8 reanalyze.py
```

The script recomputes the bilinear fits, all 35 test choices, admission/abstention, calibration-aware baselines and minimum/mean/maximum sensitivity. It writes `recomputed-results.json`. Its assertions check the primary admitted geometric regret 1.0043178222330102, complete regret 1.082678792437052, 17/19 winner agreement and the matched-payload C4 baseline regret 1.0717541430413777. NumPy uses standard least squares; last-bit platform differences are expected.

`selected-summary-matrix.csv` is the authoritative machine-readable numeric matrix: 89 configuration identities, 623 rows (six candidate arms plus a synchronization floor), raw block start-line identifiers and matching-block count. The selected complete block is the first matching block, within 0.11 ns of the five formatted values. `primary_ns` preserves the exact original fit inputs (formatted floor/pull/flat/push/global plus bound raw bulk/async minima). `min_ns`, `mean_ns` and `max_ns` preserve the selected raw summaries. These distinctions account for rounding in the retained formatted table. The JSON file mirrors the same records.

There are 49 five-repetition cells and 40 three-repetition cells. Eight single-cluster fan-pattern cells at C=4/8, B=512/4096 belong to the three-repetition batch; repetition count is not determined by single versus multiple clusters. Nominal iterations are 200 and 100 respectively, with 32 timed warm rounds in both batches. Initialization and reduction are also timed. Individual repetition samples, medians, per-arm clocks and randomized execution orders are unavailable. Min/mean/max are not confidence intervals and cannot remove fixed-order confounding.

`test-comparator-decisions.csv` records the original model choice, oracle and C4 lookup comparator for each test. Calibration uses C=2/4 and tests use C=8, within pattern and launched-cluster count. Full-rank single-cluster strata have 19 admitted tests. Sixteen multi-cluster tests abstain, retaining flat pull as the original fallback; the C4 fallback remains a labeled sensitivity policy.

`MANIFEST.json` identifies the retained raw file, kernel, sweep script and original analysis by SHA-256 and lists artifact file digests. The full source/raw files are not included in this numeric package. Source hashes establish identity, not independent correctness or public availability. This package reconstructs the numerical selection analysis; it does not reproduce GPU acquisition, check assembly, supply missing repetitions or validate the source-level ordering contract on hardware.
