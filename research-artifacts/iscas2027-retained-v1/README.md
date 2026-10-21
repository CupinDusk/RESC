# Author-approved reproducibility package, 2026-10-21

The repository owner authorized public release of the exact `hopper-retained-v1.zip` package. The archive is preserved byte for byte: SHA-256 `7edc00ab1a561f79280a860dd35a9b52aa0c0a081607ec23f9d0c7c1f7fd6077`. Unzip it to obtain `hopper-retained-v1/`; its `MANIFEST.json` records input hashes. Historical README/manifest statements that publication had not yet been authorized describe preparation time and are superseded by this release note.

This numeric artifact reanalyzes retained H20 summaries. Run `reanalyze.py` in the extracted folder with Python 3.12 and NumPy. It does not include native acquisition/source, per-repetition samples, per-arm state or randomized runs. Fixed arm order and reuse of inspected data prevent interpreting the recomputed selection scores as an independent prospective hardware validation. Public availability does not resolve those scientific limitations.

Upstream notices and applicable repository licenses continue to apply. No new license grant is asserted by this release metadata. OpenAI Codex assisted preparation and analysis.
