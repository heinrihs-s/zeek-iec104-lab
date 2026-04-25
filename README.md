# zeek-iec104-lab

Tiny helper scripts for playing with synthetic IEC-104-ish Zeek records.

This is for lab data, toy records, queue counting, and preservation checks. It does not include traffic captures and does not talk to live IEC-104 devices.

## Contents

- `scenarios/` - simple scenario templates
- `scripts/inject_zeek_records.py` - merge synthetic scenario records into toy Zeek-like logs
- `scripts/compute_queue_burden.py` - count raw and grouped queue volume
- `scripts/compute_preservation.py` - check whether tagged scenario records survive filtering
- `scripts/clustered_bootstrap.py` - small bootstrap helper
- `examples/` - toy input files

## Use

```bash
python scripts/compute_queue_burden.py examples/toy_zeek_records.csv
python scripts/inject_zeek_records.py --help
```

Everything here is boring on purpose: files in, counts out.
