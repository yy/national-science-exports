'''
This script calculates the dissimilarity of new activated disciplines
with the current research profile.

input:
-argv[1]:density of disciplines in countries across periods

output:
-argv[2]:
'''
import sys
import pandas as pd
import numpy as np
from itertools import product

DENSITY_FILE=sys.argv[1]
DENSITY_NORM_OUTPUT=sys.argv[2]


def density_zscore(data):
    meta_normed=pd.DataFrame()
    cntrylist=data.COUNTRY.unique()
    yearlist=data.CRRT_TIME.unique()
    for c, y in product(cntrylist,yearlist):
        df=data[(data.COUNTRY==c)&(data.CRRT_TIME==y)]
        if not df.empty:
            df=df[df.st0==0]
            density_avg=np.average(df.Density.values)
            density_std=np.std(df.Density.values)
            df['Density_norm']=df['Density'].apply(lambda x: (x-density_avg)/(density_std))
            meta_normed=pd.concat([meta_normed,df])
    return meta_normed

density_df=pd.read_csv(DENSITY_FILE)
# z-score of density of inactivated disciplines
meta_norm=density_zscore(density_df)

#average z-scores of activated disciplines
dissim_df=meta_norm[meta_norm.st1==1].groupby(
['COUNTRY','CRRT_TIME'])['Density_norm'].mean().reset_index()

dissim_df.to_csv(DENSITY_NORM_OUTPUT,index=False)
