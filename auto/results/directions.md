# Candidate directions (all estimate population shares from discourse only)

Baseline to beat: one-vote-per-seen-user, err_support 0.109 ± 0.005 (3 seeds). Noise floor 0.010.

A. **Change inference — inverse inclusion-probability weighting (Horvitz–Thompson/Hajek).**
   Rationale: a user is seen with prob 1-exp(-lam); weight each seen user by its inverse, with lam estimated
   from the *independent* window-B count (using kA would be circular: it's what selected them), shrunk with a
   Gamma-Poisson empirical-Bayes prior. Cheapest test: same weights with the true lam (oracle ceiling), then estimated lam.
B. **Change the data used — extrapolate along activity.** Rationale: if opinion drifts smoothly with posting rate,
   fit share vs. activity level among seen users and extrapolate to lam -> 0 (the quiet majority). Cheapest test:
   logistic regression of 1[x>0] on log(kB+0.5), predict at the low end.
C. **Change the model — full generative fit.** Rationale: fit the zero-truncated mixture (opinion bin × rate) by EM
   and read off the population, including an explicit structural-silent class. Cheapest test: 2-bin opinion, Gamma rates.

Chosen: **A**. It's the standard, explainable correction, and its oracle version tells us how much of the bias is
recoverable at all versus structural silence (pi0 people who never post are invisible to every method — the
"near-tautological" core of the bias). Expect A to remove the activity-driven part but not the pi0·delta part.
