# Review request 2 — before conclusion

Since review 1: fixed the degenerate world (v2: mu ~ U(-0.7,0.7)), fixed prior forwarding, added const baseline, reran all
methods (src/run_v2.py -> results/v2.csv), ablated eb_ipw (src/ablate.py -> results/ablate.csv), made figures (src/figures.py).
LOG entries from "00:25 Review 1 -> EVAL CHANGE" onward. REPORT.md is the draft conclusion.

Claims to check:
1. eb_ipw err_support 0.0417 ± 0.0027 vs users 0.0776 ± 0.0056 vs const 0.1299 (3 seeds); beats both beyond floor 0.011.
2. Ablation: second window essential (eb_kA 0.070 ≈ users), shrinkage helps (raw_kB 0.055), binning no clear effect.
3. Is v2 still degenerate in any way (e.g. a trivial estimator that beats eb_ipw on support)? I know const ties on extreme.
4. Do REPORT.md sections 2, 5, 7 overclaim anything vs the code/results?
