import numpy as np
import pandas as pd
from evaluate import run, weighted_shares
from baseline import EST
from dir_a import eb_weights, oracle
from dir_a2 import eb_weights_binned
from dir_c import ztnb_weights

est = {**EST,
       "const": lambda o: dict(support=0.5, extreme=0.1336),
       "eb_ipw": lambda o: weighted_shares(o, eb_weights(o)),
       "eb_ipw_binned": lambda o: weighted_shares(o, eb_weights_binned(o)),
       "ztnb_binned": lambda o: weighted_shares(o, ztnb_weights(o))}
df = pd.concat([run(est, s) for s in (1, 2, 3)] + [oracle(s) for s in (1, 2, 3)])
df.to_csv("../results/v2.csv", index=False)
per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
t = df[df.method == "users"]
print("true support range: %.2f-%.2f" % (t.true_support.min(), t.true_support.max()))
