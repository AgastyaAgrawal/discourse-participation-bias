# Review request 4 — real-data pivot

On the human's instruction I abandoned simulated data as evidence and collected real data: all Hacker News comments
2025-09-01..28 via the public Algolia API (src/collect_hn.py; data/hn_2025-09.csv.gz, usernames hashed).
Analysis: src/hn_data.py (features), src/describe_hn.py, src/predict_hn.py (pre-registered), src/predict_hn_drift.py
(pre-registered drift adjustment), src/predict_hn_ebT.py (post-hoc), src/figures_hn.py. LOG entries from "01:12 PIVOT".
REPORT.md is rewritten around the real data.

Please check:
1. Do the REPORT §2 numbers and §7 claims match the code and results files?
2. Data provenance / sampling: anything that undermines the descriptive claims (concentration, stability, capture-recapture)?
3. Is the prediction test design sound (target T, drift adjustment using returning users, folds as replicates)?
4. Anything overclaimed about "modelling the participation bias"?
