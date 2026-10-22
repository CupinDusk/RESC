# Exact synthetic local audit implementation costs

One host, synthetic exact integer log units, no timed H20 auditor or physical/GPU speedup. Complete stream primary; beta-survivor stream diagnostic. Nine blocks are repeated measures on one host, not independent systems. Preprocessing+Q totals are modeled from separately measured medians, not timed end-to-end executions. Given closed_R excludes common separately measured closure; a raw-edge direct BF alternative can avoid closure entirely. Synthetic mix weights are designed coverage, not workload prevalence.

All 870 plans / 41760 queries passed exact route, Floyd and BF certificate checks; Python independently checked37440 n≤8 queries. Shared beta rejects15567. Cheap+span falls back5288; quartet union5099,189 extra admissions. Unknown0 for these exact integer inputs.

Times below are medians ns/query; preprocessing quartets ns/plan. Crossover uses median stage differences and may fail in individual blocks. All min/max/raw values are in RESULTS.json and CSV.

|n|geometry|family|plans|cheap EXACT|quartet EXACT|direct|beta|cheap+span|quartet union|quartet preprocess|crossover Q|
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|6|contiguous|all720|720|2|40|174.9|82.5|43.4|42.8|41.0|75|
|4|contiguous|aligned|3|3|3|54.6|35.2|9.1|9.1|1.7|None|
|4|contiguous|reverse|3|3|3|56.1|37.8|9.7|9.8|3.3|None|
|4|contiguous|winner_star|3|3|3|50.8|39.9|6.6|6.5|1.7|35|
|4|contiguous|mixed_total|3|0|1|54.4|36.2|11.7|11.0|25.0|38|
|4|contiguous|sparse_dag|3|2|3|49.4|37.4|5.7|5.0|15.0|21|
|4|sparse|aligned|3|3|3|52.1|40.6|9.8|9.9|3.3|None|
|4|sparse|reverse|3|3|3|51.2|38.0|9.9|9.9|3.3|161|
|4|sparse|winner_star|3|3|3|47.3|41.1|6.6|6.6|1.7|None|
|4|sparse|mixed_total|3|0|1|51.5|41.0|17.4|15.0|25.0|11|
|4|sparse|sparse_dag|3|2|3|46.8|37.0|6.4|5.0|15.0|12|
|8|contiguous|aligned|3|3|3|248.4|110.0|29.2|28.9|1.7|7|
|8|contiguous|reverse|3|3|3|243.5|106.3|31.4|30.5|1.7|2|
|8|contiguous|winner_star|3|3|3|196.6|116.1|11.1|11.2|3.3|None|
|8|contiguous|mixed_total|3|0|0|255.4|119.1|62.0|63.2|33.3|None|
|8|contiguous|sparse_dag|3|0|0|226.9|122.6|43.4|43.2|58.3|337|
|8|sparse|aligned|3|3|3|239.1|116.4|31.8|32.5|3.3|None|
|8|sparse|reverse|3|3|3|232.6|110.6|32.1|32.1|3.3|None|
|8|sparse|winner_star|3|3|3|178.4|126.2|11.7|11.7|3.3|None|
|8|sparse|mixed_total|3|0|0|243.0|132.9|97.2|93.9|31.7|10|
|8|sparse|sparse_dag|3|0|0|213.8|128.1|60.9|60.7|55.0|221|
|16|contiguous|aligned|3|3|3|1471.7|410.7|112.4|112.0|3.3|9|
|16|contiguous|reverse|3|3|3|1519.3|375.3|108.2|108.5|3.3|None|
|16|contiguous|winner_star|3|3|3|1060.2|400.9|20.6|20.3|1.7|6|
|16|contiguous|mixed_total|3|0|0|1670.0|411.8|273.4|269.8|26.7|8|
|16|contiguous|sparse_dag|3|0|0|1407.4|443.4|234.1|236.6|731.7|None|
|16|sparse|aligned|3|3|3|1407.2|445.7|128.1|126.8|3.3|3|
|16|sparse|reverse|3|3|3|1471.2|375.6|114.7|112.7|3.3|2|
|16|sparse|winner_star|3|3|3|916.0|457.2|21.6|21.5|1.7|49|
|16|sparse|mixed_total|3|0|0|1560.3|491.4|364.7|360.0|28.3|7|
|16|sparse|sparse_dag|3|0|0|1221.9|496.5|339.5|350.8|725.0|None|
|32|contiguous|aligned|3|3|3|9695.3|1732.9|440.0|439.7|3.3|13|
|32|contiguous|reverse|3|3|3|9962.5|1457.1|413.2|413.3|3.3|None|
|32|contiguous|winner_star|3|3|3|6594.7|1497.5|40.0|40.1|3.3|None|
|32|contiguous|mixed_total|3|0|0|11243.5|1971.9|1467.5|1448.1|23.3|2|
|32|contiguous|sparse_dag|3|0|0|10321.4|1781.7|1139.0|1118.6|10121.7|496|
|32|sparse|aligned|3|3|3|9799.7|1648.3|463.3|464.3|3.3|None|
|32|sparse|reverse|3|3|3|10173.2|1369.7|411.4|403.6|5.0|1|
|32|sparse|winner_star|3|3|3|5344.2|1707.2|43.6|43.3|1.7|6|
|32|sparse|mixed_total|3|0|0|11023.2|2261.9|1783.1|1778.3|21.7|5|
|32|sparse|sparse_dag|3|0|0|8821.9|2155.7|1574.9|1643.1|10135.0|None|
|64|contiguous|aligned|3|3|3|77252.4|7729.2|1680.6|1672.2|3.3|1|
|64|contiguous|reverse|3|3|3|74297.9|6376.7|1656.9|1665.6|3.3|None|
|64|contiguous|winner_star|3|3|3|52205.2|6460.4|79.2|78.8|1.7|5|
|64|contiguous|mixed_total|3|0|0|83249.3|11977.1|9519.8|9461.8|30.0|1|
|64|contiguous|sparse_dag|3|0|0|79123.6|12450.7|9761.5|9933.0|2236.7|None|
|64|sparse|aligned|3|3|3|78544.8|6655.2|1743.4|1734.7|3.3|1|
|64|sparse|reverse|3|3|3|78577.1|5853.5|1602.8|1606.2|3.3|None|
|64|sparse|winner_star|3|3|3|51072.6|6579.5|80.9|83.7|3.3|None|
|64|sparse|mixed_total|3|0|0|85954.5|13792.0|11995.5|12005.6|31.7|None|
|64|sparse|sparse_dag|3|0|0|75629.5|18596.9|16363.2|16823.3|2251.7|None|
