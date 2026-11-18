import numpy as np
import pandas as pd
from scipy.special import gammaln
from hn_data import load, FEATS
from predict_hn import estimates

d = load()
rows = []
for f in range(3):
    df = d[d.fold == f]
    est, truth, _ = estimates(df)
    u1 = df[df.win == "W1"].groupby("user")[FEATS].mean()
    k2 = df[df.win == "W2"].groupby("user").size().reindex(u1.index, fill_value=0).values
    m, v = k2.mean(), k2.var()
    a = m**2 / (v - m); b = a / m
    lam = (a + k2) / (b + 1)
    w = np.exp(-lam) * (1 - np.exp(-2 * lam)) / (1 - np.exp(-lam))
    est["eb_T"] = u1.mul(w, axis=0).sum() / w.sum()
    seen1 = set(u1.index)
    R = df[(df.win == "W3") & df.user.isin(seen1)].user.unique()
    drift = (df[(df.win == "W3") & df.user.isin(R)].groupby("user")[FEATS].mean().mean()
             - df[(df.win == "W1") & df.user.isin(R)].groupby("user")[FEATS].mean().mean())
    for mth, e in est.items():
        for adj, e2 in [("raw", e), ("drift_adj", e + drift)]:
            rows += [dict(fold=f, method=mth, adj=adj, feat=k, signed=e2[k] - truth[k], err=abs(e2[k] - truth[k])) for k in FEATS]
r = pd.DataFrame(rows)
r.to_csv("../results/hn_predict_ebT.csv", index=False)
s = r[r.adj == "drift_adj"].groupby(["method", "feat", "fold"])[["err", "signed"]].mean().groupby(["method", "feat"]).agg(["mean", "std"])
print("DRIFT-ADJUSTED"); print(s.round(4).unstack("feat").to_string())
print("cd src && python predict_hn_ebT.py")
