import numpy as np
import pandas as pd
from evaluate import run, weighted_shares
from baseline import EST
from dir_a import eb_weights

est = {"users": EST["users"],
       "eb_ipw": lambda o: weighted_shares(o, eb_weights(o)),
       "eb_kA": lambda o: weighted_shares(o, eb_weights(dict(kB=o["kA"]))),
       "raw_kB": lambda o: weighted_shares(o, 1 / (1 - np.exp(-(o["kB"] + 0.5))))}
df = pd.concat([run(est, s) for s in (1, 2, 3)])
df.to_csv("../results/ablate.csv", index=False)
per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
for m in est:
    e = df[df.method == m]
    print(m, "mean signed support err %.4f" % (e.est_support - e.true_support).mean(), " corr(signed, c) %.2f" % np.corrcoef(e.c, e.est_support - e.true_support)[0, 1])
