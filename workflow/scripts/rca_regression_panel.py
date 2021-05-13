import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
from linearmodels.panel import PooledOLS
import sys

DATA_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

change_df=pd.read_csv(DATA_FILE)

num_period=len(change_df.period.unique())
change_df['size']=change_df.groupby('Code')['Code'].transform('size')
change_df=change_df[change_df['size']==num_period]

change_df['Income_t0_log']=np.log10(change_df['Income_t0'])
change_df=change_df.set_index(['Code','date'])

exog_vars = ['Income_t0_log','nm_change','shm_change','ne_change','sum_adv_t0']
exog = sm.add_constant(change_df[exog_vars])
mod = PanelOLS(change_df.growth_rate, exog,entity_effects=True)
fe_res = mod.fit()
with open(OUTPUT_FILE,'w') as f:
    f.write(fe_res.summary.as_text())
