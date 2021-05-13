import sys

import numpy as np
import pandas as pd

PROX_ALL = sys.argv[1]
PROX_SNAPSHOT = sys.argv[2]
SIMILARITY = sys.argv[3]

prox_all = pd.read_csv(PROX_ALL, sep="\t", names=["source", "target", "weight"])
prox_df = pd.read_csv(PROX_SNAPSHOT, sep="\t", names=["source", "target", "weight"])

prox_all = prox_all.sort_values(by=["source", "target"])
prox_df = prox_df.sort_values(by=["source", "target"])
prox_meta = prox_all.merge(prox_df, on=["source", "target"], how="outer")
prox_meta = prox_meta.fillna(0)

sim = np.corrcoef(prox_meta["weight_x"].values, prox_meta["weight_y"].values)
sim = np.round(sim, decimals=2)
np.savetxt(SIMILARITY, sim, delimiter=",")
