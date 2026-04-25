# input format

The scripts here read flat record files. CSV or JSONL, your choice.

## Required columns

- `ts` - timestamp, seconds since epoch, float
- `src` - source identifier (IP, hostname, or any string)
- `dst` - destination identifier
- `asdu_type` - integer type id
- `cot` - cause of transmission
- `ioa` - information object address

Optional:
- `tag` - free-text tag, used by `compute_preservation.py`

## CSV

Standard comma-separated, header row required. UTF-8.

## JSONL

One JSON object per line. Same field names as CSV.

## Notes

The records are deliberately not real Zeek logs. They are a small,
flat shape that is easy to generate and easy to diff. If you want to
plug in actual Zeek output, project it into this shape first.
