import numpy as np
import pandas as pd
from evaluate import run, weighted_shares
from baseline import EST
from dir_a import eb_weights


def extrap(o):
    u, p = EST["users"](o), EST["posts"](o)
    return {k: np.clip(2 * u[k] - p[k], 0, 1) for k in u}


est = {"users": EST["users"], "const": lambda o: dict(support=0.5, extreme=0.1336),
       "extrap": extrap, "eb_ipw": lambda o: weighted_shares(o, eb_weights(o))}
df = pd.concat([run(est, s) for s in (4, 5, 6)])
df.to_csv("../results/fresh_seeds.csv", index=False)
per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
w = df.pivot_table(index=["seed", "world"], columns="method", values=["err_support", "err_extreme"])
for k in ["err_support", "err_extreme"]:
    d = w[k]["extrap"] - w[k]["eb_ipw"]
    ps = d.groupby("seed").mean()
    print(f"{k}: paired extrap−eb_ipw per-seed {ps.round(4).tolist()}, mean {ps.mean():.4f} ± {ps.std():.4f}; eb_ipw better in {(d > 0).sum()}/{len(d)} worlds")
