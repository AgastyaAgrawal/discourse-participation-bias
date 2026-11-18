import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln
from evaluate import run, weighted_shares
from baseline import EST
from dir_a import eb_weights, oracle
from dir_a2 import eb_weights_binned


def p_seen_ztnb(kA, kB):
    """MLE of lam~Gamma(alpha, beta) from (kA, kB) truncated on kA>0; returns P(kA>0)."""
    K = kA + kB

    def nll(t):
        a, b = np.exp(t)
        ll = gammaln(a + K) - gammaln(a) + a * np.log(b) - (a + K) * np.log(b + 2)
        return -(ll.sum() - len(K) * np.log1p(-(b / (b + 1)) ** a))

    a, b = np.exp(minimize(nll, [0.0, 0.0], method="Nelder-Mead").x)
    return 1 - (b / (b + 1)) ** a


def ztnb_weights(o, n_bins=10):
    bins = np.digitize(o["x"], np.quantile(o["x"], np.linspace(0, 1, n_bins + 1)[1:-1]))
    w = np.empty(len(o["x"]))
    for b in range(n_bins):
        m = bins == b
        w[m] = 1 / p_seen_ztnb(o["kA"][m], o["kB"][m])
    return w


if __name__ == "__main__":
    est = {**EST,
           "eb_ipw": lambda o: weighted_shares(o, eb_weights(o)),
           "eb_ipw_binned": lambda o: weighted_shares(o, eb_weights_binned(o)),
           "ztnb_binned": lambda o: weighted_shares(o, ztnb_weights(o))}
    df = pd.concat([run(est, s) for s in (1, 2, 3)] + [oracle(s) for s in (1, 2, 3)])
    df.to_csv("../results/dir_c.csv", index=False)
    per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
    print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
    e = df[df.method == "ztnb_binned"]
    print("corr(signed err, c) ztnb: %.2f" % np.corrcoef(e.c, e.est_support - e.true_support)[0, 1])
