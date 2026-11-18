import numpy as np
import pandas as pd
from evaluate import run, weighted_shares, N_WORLDS
from world import draw_params, simulate, truth
from baseline import EST


def eb_weights(o):
    m, v = o["kB"].mean(), o["kB"].var()
    alpha = m**2 / max(v - m, 1e-6)
    lam_hat = (alpha + o["kB"]) / (alpha / m + 1)
    return 1 / (1 - np.exp(-lam_hat))


def oracle(seed):
    """Diagnostic ceiling: same worlds as run(), weights from the true lam."""
    rng = np.random.default_rng(seed)
    rows = []
    for wi in range(N_WORLDS):
        pop, obs = simulate(draw_params(rng), rng)
        t, e = truth(pop), weighted_shares(obs, 1 / (1 - np.exp(-pop["lam"][pop["seen"]])))
        rows.append(dict(seed=seed, world=wi, method="oracle_ipw", **{f"err_{k}": abs(e[k] - t[k]) for k in t}))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    est = {**EST, "eb_ipw": lambda o: weighted_shares(o, eb_weights(o))}
    df = pd.concat([run(est, s) for s in (1, 2, 3)] + [oracle(s) for s in (1, 2, 3)])
    df.to_csv("../results/dir_a.csv", index=False)
    per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
    print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
