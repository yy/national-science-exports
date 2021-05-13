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
select_df=change_df[change_df.IncomeGroup==incomegroup]

#filter out unbalanced data points
num_period=len(select_df.period.unique())
select_df['size']=select_df.groupby('Code')['Code'].transform('size')
select_df=select_df[select_df['size']==num_period]

select_df['Income_t0_log']=np.log10(select_df['Income_t0'])
select_df=select_df.set_index(['Code','date'])

exog_vars = ['Income_t0_log','nm_change','shm_change','ne_change','sum_adv_t0']
exog = sm.add_constant(select_df[exog_vars])
mod = PanelOLS(select_df.growth_rate, exog,entity_effects=True)
fe_res = mod.fit()
with open(OUTPUT_FILE,'w') as f:
    f.write(fe_res.summary.as_text())
