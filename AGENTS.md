# Agent Instructions

This repository contains tiny helper scripts for synthetic IEC-104-style Zeek records.

## Safety Rules

- Do not add live capture, packet sending, target probing, or connection features.
- Keep scripts file-in/file-out.
- Preserve the current refusal behavior for live-target-looking arguments.
- Keep examples synthetic.

## Good Agent Tasks

- Add toy scenarios and expected output fixtures.
- Improve CSV input validation.
- Add tests for queue burden and preservation calculations.
- Add documentation for converting lab-only records into repeatable examples.

## Verification

```bash
python -m compileall scripts
python scripts/compute_queue_burden.py examples/toy_zeek_records.csv
```
