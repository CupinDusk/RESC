# Independent changing-clock model validation

Actual result: **PASS**, with no failed assertions. This checks the specified digital-source model and serialized numerical certificates. It is not RTL, silicon, GPU acquisition, timing, speedup, or physical calibration evidence.

- `validate_changing_clock_independently.py`: executable stdlib Fraction/atanh and independent graph checker. It never reads, imports, or runs the new producer or `audit_core.py`.
- `VALIDATION.json`: exact results, counters, per-case totals, input hashes, mutation outcomes, and limitations.
- `ARGUMENT.md`: mathematical derivation, population accounting, source-interface assumptions, and certificate interpretation.
- `MANIFEST.json`: input and independent-output SHA256 bindings; excludes self-hashing.

All 17,304 legal-path audit records are checked: 6,360 admissions and 10,944 rejections, with zero unresolved numerical decisions. All 2,184 true reports are admitted. The 4,176 incorrect-but-admitted reports are preserved. The box baseline admits 39 reports whose common-path audit rejects, including one fixed partial.

The checker verifies 289 scaled outward log bounds with exact rational series enclosures, 144 guard-attaining controller edges, 144 exact durations, 144 path-specific timer rectangles, every admitted witness in the original variables, every negative-cycle edge and sum, all threshold/truth flags, and exact permutation coverage. Nine predicate mutation controls are detected; synthetic uncertainty controls exercise `unknown`.

The failed-guard control has exactly bad edges 2 and 3. Its separate 5,768 report dispatches all return `contract-unknown` before numerical audit. They are not part of the 17,304-record legal audit stream.

The new protocol omitted an explicit slot-name mapping. A post-generation addendum records the inherited R03 mapping `P1,S2,B3,G4,A5,F6`; the checker independently reads and compares the prior protocol. This documentation repair is explicitly distinguished from prospective protocol specification. No original protocol, observation, or report bytes were changed.

Run from the workspace root in PowerShell:

```powershell
python -B -X utf8 run_r04_checks.py
```

The default run creates `VALIDATION.json` with exclusive creation and refuses to overwrite it. To retain a separate repeat report, pass `--output VALIDATION_REPEAT.json` with a previously unused name. Output paths are constrained to this independent directory. No remote access, timing workload, manuscript, paper source, figure, publication artifact, or top-level README was changed by this validation.
