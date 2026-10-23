# Joint-timing reproduction supplement, version6

This fixed research tree retains all previous reference studies and adds actual
PicoRV32 firmware/source-contract evidence and a fair specialized CPU baseline.
It contains research code, inputs, exact certificates and saved results, not a
paper or a claim of physical hardware validation.

`r06/picorv32/DELIVERY.md` describes the fixed public ISC-licensed CPU source,
36 firmware images,72 input/firmware combinations,576 scheduled jobs and96
reports. The actual CPU/controller models were independently synthesized and
executed. All69888 certificates were independently checked. The total-order
study retains63 extra rejections/3021 box admissions and1806 false admissions;
all768 partial queries add zero rejections and retain45 false admissions.
This is logical host composition with trusted guard/memory/scheduler
obligations, not autonomous physical clock, GPU, silicon, PPA, compiler/ISA
formal verification, confidentiality or cryptographic evidence.

`r06/specialized/` contains the single new3240-row timing collection, with the
complete schedule and repaired positive-coordinate guard. Preparation is
included; these designed inputs do not establish representative performance.
Previous timing collections remain unchanged and are not retimed.

The original fixed source license is retained. No host exe/PDB, private source,
server configuration, credentials, manuscript, figure or review is included.
Only explicitly recorded local path metadata is made portable. Earlier root
documentation and manifest are retained under r06/previous-root-*.

Run `python -B -X utf8 run_r06_checks.py --out NEW_DIRECTORY` for complete
manifest and saved-evidence checks. Full native reproduction uses the explicit
external tool arguments in r06/picorv32/replay_portable.py; tool runtimes are
not bundled. Independent actual-native validation applies to the byte-identical
payload and is separately recorded; a manifest check alone is not that audit.
