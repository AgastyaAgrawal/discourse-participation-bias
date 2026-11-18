import numpy as np
import pandas as pd
from evaluate import run, weighted_shares

EST = {
    "posts": lambda o: weighted_shares(o, o["kA"].astype(float)),
    "users": lambda o: weighted_shares(o, np.ones(len(o["x"]))),
}

if __name__ == "__main__":
    df = pd.concat([run(EST, s) for s in (1, 2, 3)])
    df.to_csv("../results/baseline.csv", index=False)
    per_seed = df.groupby(["method", "seed"])[["err_support", "err_extreme"]].mean()
    print(per_seed)
    print(per_seed.groupby("method").agg(["mean", "std"]).round(4))
