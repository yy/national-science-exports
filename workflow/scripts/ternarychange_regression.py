import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
from linearmodels.panel import PooledOLS
import sys
import ast

TERDATA=sys.argv[1]
GDPFILE=sys.argv[2]
EXOG=sys.argv[3]
OUTPUT=sys.argv[4]


ternarydata=pd.read_csv(TERDATA)
gdp=pd.read_csv(GDPFILE)

ternarydata=ternarydata.merge(
    gdp,right_on=['Code','Year'], left_on=['Country Code','YEAR'], how='inner')
ternarydata=ternarydata.dropna()
yearlist=['1973-1977','2013-2017']

change_df=pd.DataFrame()
for index, start in enumerate(yearlist[:-1]):
    end=yearlist[index+1]
    ter_start=ternarydata[ternarydata.YEAR==start]
    ter_end=ternarydata[ternarydata.YEAR==end]
    termeta=ter_start.merge(ter_end, on='Country Code',how="inner")
    termeta=termeta.dropna()
    termeta['nm_change']=termeta['NM_y']-termeta['NM_x']
    termeta['shm_change']=termeta['SHM_y']-termeta['SHM_x']
    termeta['ne_change']=termeta['NE_y']-termeta['NE_x']
    termeta['net_change']=termeta['ne_change']-termeta['nm_change']
    termeta['growth_rate']=(termeta['Income_y']-termeta['Income_x'])/(termeta['Income_x'])
    termeta['date']=index
    temp_df=termeta[
        ['Country Code','date','nm_change','shm_change','ne_change','net_change','Income_x','Income_y','growth_rate']]
    change_df=pd.concat([change_df,temp_df])

change_df = change_df.sort_values(
    by=['Country Code','date'])
change_df = change_df.set_index(['Country Code','date'])
change_df['log_income']=np.log10(change_df['Income_x'])

exog_vars=EXOG.split(",")
exog = sm.add_constant(change_df[exog_vars])
mod = PooledOLS(change_df.growth_rate, exog)
fe_res = mod.fit()
with open(OUTPUT, 'w') as fh:
    fh.write(fe_res.summary.as_text())
