import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
from linearmodels.panel import PooledOLS
import sys
import os

DATA_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

change_df=pd.read_csv(DATA_FILE)
base = os.path.basename(OUTPUT_FILE)
incomegroup = base.split(".")[0].split("_")[-1]
change_df=change_df[change_df.IncomeGroup==incomegroup]
change_df=change_df.set_index(['Code','date'])

exog_vars = ['Income_t0_log','nm_change','shm_change','ne_change','sum_adv_t0']
exog = sm.add_constant(change_df[exog_vars])
mod = PanelOLS(change_df.growth_rate, exog)
fe_res = mod.fit()
with open(OUTPUT_FILE,'w') as f:
    f.write(fe_res.summary.as_text())
