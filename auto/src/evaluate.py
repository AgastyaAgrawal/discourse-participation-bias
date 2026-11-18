import numpy as np
import pandas as pd
from world import draw_params, simulate, truth, DEV_PRIOR

N_WORLDS = 30


def weighted_shares(obs, w):
    w = w / w.sum()
    return dict(support=np.sum(w * (obs["x"] > 0)), extreme=np.sum(w * (np.abs(obs["x"]) > 1.5)))


def run(estimators, seed, prior=DEV_PRIOR):
    """estimators: {name: f(obs) -> dict(support=, extreme=)}. Same worlds for every estimator."""
    rng = np.random.default_rng(seed)
    rows = []
    for wi in range(N_WORLDS):
        p = draw_params(rng, prior)
        pop, obs = simulate(p, rng)
        t = truth(pop)
        for name, f in estimators.items():
            est = f(obs)
            rows.append(dict(seed=seed, world=wi, method=name, n_seen=len(obs["x"]), **p,
                             **{f"true_{k}": t[k] for k in t}, **{f"est_{k}": est[k] for k in t},
                             **{f"err_{k}": abs(est[k] - t[k]) for k in t}))
    return pd.DataFrame(rows)
