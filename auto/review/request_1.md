# Review request 1 — setup, evaluation, baseline

PLAN.md gives only the question ("model the bias that discourse participants are the kind of people who participate"),
no data or metric. I turned it into a simulation estimation task; please check the framing is sensible and the eval is sound.

What I did:
- src/world.py: world generator. Opinion x~N(0,1); a fraction pi0 never posts (opinion shifted by delta); others post
  Poisson(lam) per window with log lam = a + b|x| + c x + s·noise. We see only users with ≥1 post in window A: (x, kA, kB).
- src/evaluate.py (frozen): 30 worlds per seed; targets support=P(x>0) (primary), extreme=P(|x|>1.5) (secondary); metric mean abs error.
- src/baseline.py: post-weighted and per-user shares, seeds 1–3. Results in results/baseline.csv, log in results/LOG.md.
- results/directions.md: three directions; I chose A (inverse inclusion-probability weighting using window-B counts).

Claims to check:
1. Baseline: users err_support 0.1089 ± 0.0050, posts 0.2053 ± 0.0109 (3 seeds). Noise floor 0.010.
2. Eval cannot leak truth into estimators (estimators only receive obs dict).
3. Using window-B counts to estimate lam avoids the circularity of using kA.
Biggest worry: is the simulation rigged so that direction A trivially wins? Is the world prior reasonable?

## Added 00:05 — first real result (direction A)
- src/dir_a.py, results/dir_a.csv, LOG entry "23:58 Direction A".
- eb_ipw err_support 0.0622 ± 0.0055 vs users 0.1089 ± 0.0050 (3 seeds); err_extreme 0.0315 vs 0.0886.
- oracle_ipw (true lam; diagnostic ceiling only, not a method) 0.0174 ± 0.0007.
- Note: I added `seen` to the *population* dict returned by world.simulate (truth side, needed only for the oracle).
  Re-ran baseline: identical numbers. Please confirm no estimator can access pop.
- Diagnosis: eb_ipw signed error correlates 0.81 with c (opinion tilt of rate) -> under-correction from shrinking
  every user's lam toward one global mean. Next planned fix: fit the Gamma prior within opinion deciles.
