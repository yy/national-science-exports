import sys

import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

DATA_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

change_df = pd.read_csv(DATA_FILE)
change_df = change_df.set_index(["Code", "date"])

exog_vars = ["Income_t0_log", "nm_change", "shm_change", "ne_change", "sum_adv_t0"]
exog = sm.add_constant(change_df[exog_vars])
mod = PanelOLS(change_df.growth_rate, exog)
fe_res = mod.fit()
with open(OUTPUT_FILE, "w") as f:
    f.write(fe_res.summary.as_text())
