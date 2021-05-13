import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

TER_FILE=sys.argv[1]
GDP_FILE=sys.argv[2]
OUTPUT_FILE=sys.argv[3]

ternarydata = pd.read_csv(TER_FILE)
ter_begin=ternarydata[ternarydata.YEAR=="1973-1977"][['Country Code','NE','NM','SHM']]
ter_begin.columns=['country','ne_1973','nm_1973','shm_1973']
ter_recent=ternarydata[ternarydata.YEAR=="2013-2017"][['Country Code','NE','NM','SHM']]
ter_recent.columns=['country','ne_2013','nm_2013','shm_2013']

ter_meta=ter_begin.merge(ter_recent, on='country',how="inner")
ter_meta['ne_change']=ter_meta['ne_2013']-ter_meta['ne_1973']
ter_meta['nm_change']=ter_meta['nm_2013']-ter_meta['nm_1973']
ter_meta['shm_change']=ter_meta['shm_2013']-ter_meta['shm_1973']

gdp = pd.read_csv(GDP_FILE)
gdp_growth=gdp[gdp.Year.isin(['1973-1977','2013-2017'])]
gdp_growth = gdp_growth.pivot(index="Code",columns='Year',values='Income').reset_index()
gdp_growth.columns=['country','income_1973-1977','income_2013-2017']
gdp_growth=gdp_growth.dropna()

ter_meta=ter_meta.merge(gdp_growth, on='country',how='inner')
ter_meta['income_growth']=(ter_meta['income_2013-2017']-ter_meta['income_1973-1977'])/(
    ter_meta['income_1973-1977'])
ter_meta['growth_log']=ter_meta['income_growth'].apply(lambda x:np.log(x))
ter_meta['income_2013_log']=ter_meta['income_2013-2017'].apply(lambda x:np.log10(x))
ter_meta.to_csv(OUTPUT_FILE, index=False)
