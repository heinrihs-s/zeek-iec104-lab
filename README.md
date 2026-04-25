# zeek-iec104-lab

Tiny helper scripts for playing with synthetic IEC-104-ish Zeek records.

This is for lab data, toy records, queue counting, and preservation checks.
It does not include traffic captures and does not talk to live IEC-104 devices.

## Layout

- `scenarios/` - simple scenario templates
- `scripts/inject_zeek_records.py` - merge synthetic scenario records into toy Zeek-like logs
- `scripts/compute_queue_burden.py` - count raw and grouped queue volume
- `scripts/compute_preservation.py` - check whether tagged scenario records survive filtering
- `scripts/clustered_bootstrap.py` - small bootstrap helper
- `examples/` - toy input files
- `docs/input_format.md` - input record shape
- `docs/safety.md` - what these scripts will and will not do

## Requirements

Python 3.9+. Standard library only.

## Use

```bash
$ python scripts/compute_queue_burden.py examples/toy_zeek_records.csv
raw_count 10
# top peer pairs
pair 10.0.0.1 -> 10.0.0.2 8
pair 10.0.0.2 -> 10.0.0.1 2
# top asdu types
asdu_type 1 3
asdu_type 100 2
asdu_type 45 2
asdu_type 46 2
asdu_type 3 1
```

Each script has `--help`. Each script refuses to run if you pass anything that
looks like a live target (`--host`, `--ip`, `--target`, `--port`, `--connect`,
`--send`). See `docs/safety.md`.

Everything here is boring on purpose: files in, counts out.

## License

MIT. See `LICENSE`.
