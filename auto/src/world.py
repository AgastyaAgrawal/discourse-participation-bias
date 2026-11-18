import numpy as np

DEV_PRIOR = dict(mu=(-0.7, 0.7), a=(-3, -1), b=(0, 1.5), c=(-0.7, 0.7), s=(0.5, 1.5), pi0=(0, 0.3), delta=(-0.5, 0.5))


def draw_params(rng, prior=DEV_PRIOR):
    return {k: rng.uniform(*v) for k, v in prior.items()}


def simulate(p, rng, n=50_000):
    """Population of n people; returns full population and the discourse-visible subset."""
    silent = rng.random(n) < p["pi0"]                      # structural non-participants
    x = p["mu"] + rng.normal(0, 1, n) + p["delta"] * silent          # opinion
    loglam = p["a"] + p["b"] * np.abs(x) + p["c"] * x + p["s"] * rng.normal(0, 1, n)
    lam = np.where(silent, 0.0, np.exp(loglam))             # posts per window
    kA, kB = rng.poisson(lam), rng.poisson(lam)             # two observation windows
    seen = kA > 0                                           # discourse = authors of window-A posts
    return dict(x=x, lam=lam, silent=silent, seen=seen), dict(x=x[seen], kA=kA[seen], kB=kB[seen])


def truth(pop):
    x = pop["x"]
    return dict(support=np.mean(x > 0), extreme=np.mean(np.abs(x) > 1.5))

# Held-out generalization prior (more rate heterogeneity, more silence). Not run until the human says so.
TEST_PRIOR = dict(DEV_PRIOR, s=(1.5, 2.5), pi0=(0.3, 0.5))
