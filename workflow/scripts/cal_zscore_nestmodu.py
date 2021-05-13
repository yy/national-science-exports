"""calculate zscore of nestednesss and modularity
"""

import pandas as pd
import numpy as np
import sys

NESTMODU_FILE_PATH = sys.argv[1]
YEARS_FILE_PATH = sys.argv[2]
ZSCORE_FILE_PATH = sys.argv[3]


nest_df = pd.read_csv(NESTMODU_FILE_PATH)
with open(YEARS_FILE_PATH) as f:
    yearlist = f.read().splitlines()

zlist = []
for period in yearlist:
    nest_modu_period = nest_df[nest_df.YEAR==period]
    act_nest = nest_modu_period[nest_modu_period.Flag=="Actual"]['NodfRes'].values[0]
    act_modu = nest_modu_period[nest_modu_period.Flag=="Actual"]['ModuRes'].values[0]
    null_nest = nest_modu_period[nest_modu_period.Flag=="Null"]['NodfRes'].tolist()
    null_modu = nest_modu_period[nest_modu_period.Flag=="Null"]['ModuRes'].tolist()
    nest_mean = np.mean(null_nest)
    nest_std = np.std(null_nest)
    modu_mean = np.mean(null_modu)
    modu_std = np.std(null_modu)
    z_nest = (act_nest-nest_mean)/nest_std
    z_modu = (act_modu-modu_mean)/modu_std
    zlist.append([period,z_nest,z_modu])

pd.DataFrame(zlist, columns=['YEAR','ZNEST','ZMODU']).to_csv(ZSCORE_FILE_PATH, index=False)