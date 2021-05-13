import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
from linearmodels.panel import PooledOLS
import sys

RCA_FILE = sys.argv[1]
DSCP_FILE = sys.argv[2]
GDP_FILE = sys.argv[3]
FLAG_TABLE = sys.argv[4]
CNTRY_INCOMEGROUP=sys.argv[5]
OUTPUT_FILE = sys.argv[6]

def get_panel_data(data, yearlist):
    change_df=pd.DataFrame()
    for index, start in enumerate(yearlist[:-1]):
        end=yearlist[index+1]
        data_start=data[data.Year==start]
        data_end=data[data.Year==end]
        datameta=data_start.merge(data_end, on='Code',how="inner")
        datameta=datameta.dropna()
        datameta['nm_change']=datameta['NM_y']-datameta['NM_x']
        datameta['shm_change']=datameta['SHM_y']-datameta['SHM_x']
        datameta['ne_change']=datameta['NE_y']-datameta['NE_x']
        datameta['growth_rate']=np.log10((datameta['Income_y'])/(datameta['Income_x']))
        datameta['date']=index
        temp_df=datameta[
            ['Code','date','nm_change','shm_change','ne_change','Income_x','sum_adv_x','growth_rate']]
        change_df=pd.concat([change_df,temp_df])
    change_df=change_df.dropna()
    change_df= change_df[change_df.groupby(
    'Code')['Code'].transform('size')==(len(yearlist)-1)]
    change_df['Income_x_log']=np.log10(change_df['Income_x'])
    change_df = change_df.sort_values(by=['Code','date'])
    return change_df

rca_df=pd.read_csv(RCA_FILE)
rca_df=rca_df.query('VALUES>1')
dscp=pd.read_csv(DSCP_FILE,names=['DIS','GROUP'],sep="\t")
gdp=pd.read_csv(GDP_FILE)
flag_df = pd.read_csv(FLAG_TABLE, sep="\t")
incomegroup=pd.read_csv(CNTRY_INCOMEGROUP)

rca_df=rca_df.merge(dscp, on='DIS')
cntry_adv=rca_df.groupby(['COUNTRY','YEAR','GROUP']).size().reset_index()
cntry_adv.columns=['cntry','year','group','count']
cntry_adv = cntry_adv.pivot_table(index=['cntry','year'],columns='group').reset_index().fillna(0)
cntry_adv.columns = cntry_adv.columns.droplevel()
cntry_adv.columns=['cntry','Year','NE','NM','SHM']
cntry_adv=cntry_adv.merge(flag_df[['WoS','Code']],left_on="cntry",right_on="WoS")


cntry_adv=cntry_adv.merge(
    gdp,on=['Code','Year'],how='inner')
cntry_adv['sum_adv']=cntry_adv['NE']+cntry_adv['NM']+cntry_adv['SHM']
change_df=get_panel_data(cntry_adv,['1973-1977','2013-2017'])
change_df=change_df.rename(columns={'Income_x':'Income_t0','sum_adv_x':'sum_adv_t0','Income_x_log':'Income_t0_log'})
income_initial=incomegroup[incomegroup.YEAR=="1988-1992"][['Code','IncomeGroup']]
change_df = change_df.merge(income_initial,on="Code",how='inner')
change_df.to_csv(OUTPUT_FILE,index=False)
