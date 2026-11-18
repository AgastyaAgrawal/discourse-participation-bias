import numpy as np
import pandas as pd
from evaluate import run, weighted_shares
from baseline import EST
from dir_a import eb_weights, oracle


def eb_weights_binned(o, n_bins=10):
    bins = np.digitize(o["x"], np.quantile(o["x"], np.linspace(0, 1, n_bins + 1)[1:-1]))
    w = np.empty(len(o["x"]))
    for b in range(n_bins):
        m = bins == b
        w[m] = eb_weights(dict(kB=o["kB"][m]))
    return w


if __name__ == "__main__":
    est = {**EST,
           "eb_ipw": lambda o: weighted_shares(o, eb_weights(o)),
           "eb_ipw_binned": lambda o: weighted_shares(o, eb_weights_binned(o))}
    df = pd.concat([run(est, s) for s in (1, 2, 3)] + [oracle(s) for s in (1, 2, 3)])
    df.to_csv("../results/dir_a2.csv", index=False)
    per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
    print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
    e = df[df.method == "eb_ipw_binned"]
    print("corr(signed err, c) binned: %.2f" % np.corrcoef(e.c, e.est_support - e.true_support)[0, 1])
