import pandas as pd
import numpy as np
import sys
import statsmodels.formula.api as smf
import os
from statsmodels.iolib.summary2 import summary_col
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from linearmodels import PanelOLS
from linearmodels import RandomEffects



if __name__ == "__main__":
    REG_DATA = sys.argv[1]
    RES3_PATH = sys.argv[2]

    metadata=pd.read_csv(REG_DATA)
    metadata = metadata.sort_values(by=['Code','Year'])
    metadata=metadata.set_index(['Code','Year'])
    metadata['Income_t0_log']=np.log10(metadata['Income_t0'])


    base = os.path.basename(RES3_PATH)
    incomegroup = base.split(".")[0].split("_")[-1]
    metadata = metadata[metadata.IncomeGroup==incomegroup]
    metadata=metadata.dropna()

    num_period=len(metadata['period'].unique())
    metadata=metadata[metadata['size']==num_period]


    exog_vars = ['ECI','Income_t0_log','diversity']
    exog = sm.add_constant(metadata[exog_vars])
    mod = RandomEffects(metadata.growth,exog)
    with open(RES3_PATH,'w') as f:
        f.write(mod.fit().summary.as_text())
