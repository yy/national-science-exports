"""this script runs the regression

input:
-argv[1]: regression table

output:
-argv[2]: regression result

"""

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
    RES1_PATH = sys.argv[2]
    RES2_PATH = sys.argv[3]
    RES3_PATH = sys.argv[4]

    metadata=pd.read_csv(REG_DATA)
    metadata = metadata.sort_values(by=['Code','Year'])
    metadata=metadata.set_index(['Code','Year'])
    metadata['Income_t0_log']=np.log10(metadata['Income_t0'])

    num_period=len(metadata['period'].unique())



    data=metadata[['growth','Income_t0_log','size']].copy()
    data=data.dropna()
    data=data[data['size']==num_period]
    exog_vars = ['Income_t0_log']
    exog = sm.add_constant(data[exog_vars])
    mod = PanelOLS(data.growth,exog,entity_effects=True)
    with open(RES1_PATH,'w') as f:
        f.write(mod.fit().summary.as_text())

    data=metadata[['growth','Income_t0_log','size','ECI']].copy()
    data=data.dropna()
    data=data[data['size']==num_period]
    exog_vars = ['ECI','Income_t0_log']
    exog = sm.add_constant(data[exog_vars])
    mod = PanelOLS(data.growth,exog,entity_effects=True)
    with open(RES2_PATH,'w') as f:
        f.write(mod.fit().summary.as_text())

    data=metadata[['growth','Income_t0_log','size','ECI','diversity']].copy()
    data=data.dropna()
    data=data[data['size']==num_period]
    exog_vars = ['ECI','Income_t0_log','diversity']
    exog = sm.add_constant(data[exog_vars])
    mod = PanelOLS(data.growth,exog,entity_effects=True)
    with open(RES3_PATH,'w') as f:
        f.write(mod.fit().summary.as_text())
