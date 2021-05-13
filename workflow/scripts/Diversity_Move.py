import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlrd
import numpy as np
import sys
import itertools


FLAG_TABLE=sys.argv[1]
ST_TABLE=sys.argv[2]
GINI_FILE = sys.argv[3]
INCOME_FILE=sys.argv[4]

gini_df=pd.read_csv(GINI_FILE)
income_df=pd.read_csv(INCOME_FILE)
flag_table=pd.read_csv(FLAG_TABLE, sep="\t")
st_table=pd.read_csv(ST_TABLE, sep="\t", names=['WoS','st'])

gini_df=gini_df.merge(
    flag_table[['WoS','Code']],left_on="COUNTRY", right_on="WoS")
income_df = income_df.rename(columns={'Year':'YEAR'})
metadata=gini_df[['Code','GINI','YEAR','ST']].merge(income_df, on=['Code','YEAR'])
metadata['Diversity']=1-metadata['GINI']
metadata.dropna(inplace=True)


ybins=np.arange(0,140000,10000)
ylabels=np.arange(10000,140000,10000)
xbins=np.arange(0,10,1)/10
xlabels=np.arange(1,10,1)/10
metadata['ybins'] = pd.cut(
    metadata['Income'], bins=ybins, labels=ylabels)
metadata['xbins'] = pd.cut(
    metadata['Diversity'], bins=xbins, labels=xlabels)

x_start=[]
y_start=[]
x_end=[]
y_end=[]
for xgrid, ygrid in itertools.product(xlabels, ylabels):
    cell_df = metadata[(metadata.xbins==xgrid) &(metadata.ybins==ygrid)]
    cell_df = cell_df[cell_df.YEAR!="2013-2017"]
    current_df= pd.DataFrame()
    next_df = pd.DataFrame()
    for index, row in cell_df.iterrows():
        cntry_code=row['Code']
        year_crrt=row['YEAR']
        year_next_index=yearorder.index(year_crrt)+1
        cntry_next=metadata[
            (metadata.Code==cntry_code) & (metadata.YEAR==yearorder[year_next_index])]
        if not cntry_next.empty:
            current_df = pd.concat([current_df, cell_df.loc[[index]]])
            next_df = pd.concat([next_df, cntry_next])
    if not current_df.empty:
        x_start.append(current_df.Diversity.mean())
        y_start.append(current_df.Income.mean())

        x_end.append(next_df.Diversity.mean())
        y_end.append(next_df.Income.mean())
