import numpy as np
import pandas as pd
from hn_data import load, FEATS
from dir_a import eb_weights


def estimates(d):
    w1 = d[d.win == "W1"]
    u1 = w1.groupby("user")[FEATS].mean()
    k2 = d[d.win == "W2"].groupby("user").size().reindex(u1.index, fill_value=0).values
    w = eb_weights(dict(kB=k2))                       # 1/(1-e^-lam_hat)
    w_unseen = w - 1                                  # = e^-lam/(1-e^-lam)
    posts, users = w1[FEATS].mean(), u1.mean()
    est = {"posts": posts, "users": users, "extrap": 2 * users - posts,
           "eb_unseen": (u1.mul(w_unseen, axis=0)).sum() / w_unseen.sum()}
    seen1 = set(u1.index)
    w3 = d[(d.win == "W3") & ~d.user.isin(seen1)]
    truth = w3.groupby("user")[FEATS].mean().mean()
    return est, truth, dict(n_w1_users=len(u1), n_target_users=w3.user.nunique())


if __name__ == "__main__":
    d = load()
    rows = []
    for f in range(3):
        est, truth, n = estimates(d[d.fold == f])
        for m, e in est.items():
            rows += [dict(fold=f, method=m, feat=k, est=e[k], truth=truth[k], err=abs(e[k] - truth[k]), **n) for k in FEATS]
    r = pd.DataFrame(rows)
    r.to_csv("../results/hn_predict.csv", index=False)
    s = r.groupby(["feat", "method", "fold"]).err.mean().groupby(["feat", "method"]).agg(["mean", "std"])
    print(s.unstack("feat").round(4).to_string())
    print(r[r.method == "users"].groupby("feat")[["truth"]].mean().round(4).T)
    print(r.groupby("fold")[["n_w1_users", "n_target_users"]].first())
    print("cd src && python predict_hn.py")
