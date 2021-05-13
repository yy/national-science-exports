""" This script prepares the regression table.
input:
-argv[1]: Aggregated gini file contains the gini value for countries
over all the time period
-argv[2]: ECI index file
-argv[3]: GDP data
-argv[4]: name flag file helps connect gini, eci and gdp
-argv[5]: publication count file

output:
-argv[6]: regression tables with all the variable
"""
import pandas as pd
import sys
import numpy as np

def construct_gdpgrowth(data,yearlist):
    gdp_growth=pd.DataFrame()
    for index, year in enumerate(yearlist[:-1]):
        t1=yearlist[index+1]
        gdp_t0=data[data.Year==year][['Code','Income']]
        gdp_t0.columns=['Code','Income_t0']
        gdp_t1=data[data.Year==t1][['Code','Income']]
        gdp_t1.columns=['Code','Income_t1']
        gdp_meta=gdp_t0.merge(gdp_t1,on='Code',how='inner').dropna()
        gdp_meta['growth']=np.log10(gdp_meta['Income_t1']/gdp_meta['Income_t0'])
        gdp_meta['Year']=year
        gdp_growth=pd.concat([gdp_growth,gdp_meta[['Code','Year','growth','Income_t0','Income_t1']]])
    return gdp_growth

def construct_eciperiod(data, yearlist):
    eciperiod=pd.DataFrame()
    for year in yearlist:
        start,end=year.split("-")
        data_filter=data[data.Year.between(int(start),int(end))]
        data_filter=data_filter.groupby('Code')['ECI'].mean().reset_index()
        data_filter['Year']=year
        eciperiod=pd.concat([eciperiod, data_filter])
    return eciperiod


if __name__ == "__main__":
    GINI_DATA = sys.argv[1]
    ECI_DATA = sys.argv[2]
    INCOME_DATA = sys.argv[3]
    FLAG_TABLE = sys.argv[4]
    YEARFILE=sys.argv[5]
    CNTRY_INCOMEGROUP=sys.argv[6]
    REG_TABLE = sys.argv[7]

    yearlist=[]
    with open(YEARFILE) as f:
        for line in f.readlines():
            yearlist.append(line.strip('\n'))

    gdp_df=pd.read_csv(INCOME_DATA)
    gdp_growth=construct_gdpgrowth(gdp_df, yearlist)

    eci=pd.read_csv(ECI_DATA)
    flag=pd.read_csv(FLAG_TABLE,sep="\t")
    eci=eci.merge(flag[['ECI_Country','Code']],
              left_on='Country',right_on='ECI_Country',how='inner')
    eciperiod = construct_eciperiod(eci,yearlist)

    gini=pd.read_csv(GINI_DATA)
    gini=gini[gini.YEAR!='1973-2017']
    gini=gini.merge(flag[['WoS','Code']], left_on='COUNTRY', right_on='WoS',how='inner')
    gini=gini[['Code','YEAR','GINI']]
    gini.columns=['Code','Year','gini']

    metadata=gini.merge(eciperiod, on=['Code','Year'],how='left')
    metadata=metadata.merge(gdp_growth, on=['Code','Year'],how='left')
    metadata=metadata[metadata.Year!='2013-2017']

    metadata['size']=metadata.groupby('Code')['Year'].transform('size')
    metadata['period']=metadata['Year']
    metadata['Year']=metadata['Year'].apply(lambda x:yearlist.index(x))
    metadata['diversity']=1-metadata['gini']

    incomegroup=pd.read_csv(CNTRY_INCOMEGROUP)
    income_initial=incomegroup[incomegroup.YEAR=="1988-1992"][['Code','IncomeGroup']]
    metadata=metadata.merge(income_initial,on='Code',how='left')

    metadata.to_csv(REG_TABLE,index=False)
