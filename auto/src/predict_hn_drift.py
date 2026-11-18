import pandas as pd
from hn_data import load, FEATS
from predict_hn import estimates

d = load()
rows = []
for f in range(3):
    df = d[d.fold == f]
    est, truth, _ = estimates(df)
    seen1 = set(df[df.win == "W1"].user)
    R = df[(df.win == "W3") & df.user.isin(seen1)].user.unique()
    r1 = df[(df.win == "W1") & df.user.isin(R)].groupby("user")[FEATS].mean().mean()
    r3 = df[(df.win == "W3") & df.user.isin(R)].groupby("user")[FEATS].mean().mean()
    for m, e in est.items():
        for adj, e2 in [("raw", e), ("drift_adj", e + r3 - r1)]:
            rows += [dict(fold=f, method=m, adj=adj, feat=k, signed=e2[k] - truth[k], err=abs(e2[k] - truth[k])) for k in FEATS]
r = pd.DataFrame(rows)
r.to_csv("../results/hn_predict_drift.csv", index=False)
s = r.groupby(["adj", "method", "feat", "fold"])[["err", "signed"]].mean().groupby(["adj", "method", "feat"]).agg(["mean", "std"])
print(s.round(4).unstack("feat").to_string())
print("cd src && python predict_hn_drift.py")
