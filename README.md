# QgcLogs

This folder contains PX4 ULog flight logs and per-topic CSV exports.

## Analyze a flight (CSV already exported)

Example 1:

```bash
python3 analyze_flight.py --logdir csv/log_41_2026-1-8-22-52-32 --plots --report
```

Example 2 (time window in seconds, relative to t=0):

```bash
python3 analyze_flight.py --logdir csv/log_45_2026-1-8-22-56-20 --start 10 --end 50 --plots --report
```

