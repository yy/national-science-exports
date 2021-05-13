"""
This script plot correlation between eci, gini and income

input:
-argv[1]: gini file for a specific period
-argv[2]: file contains eci value of country
-argv[3]: income file for countries
-argv[4]: flag table contains name variation for countries

output:
-argv[5]: plot path for gini vs eci
-argv[6]: plot path for gini vs income
-argv[7]: plot path for eci vs income
"""
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nsp.core
import numpy as np
import statsmodels.api as sm
import matplotlib as mpl
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from adjustText import adjust_text



GINI_FILE_PATH = sys.argv[1]
ECI_FILE_PATH = sys.argv[2]
INCOME_FILE_PATH = sys.argv[3]
FLAG_TABLE_PATH = sys.argv[4]
PUBCNT_PATH = sys.argv[5]

GINI_ECI_PLOT = sys.argv[6]
GINI_INCOME_PLOT = sys.argv[7]
INCOME_ECI_PLOT = sys.argv[8]
PUBCNT_GINI_PLOT = sys.argv[9]
PUBCNT_INCOME_PLOT = sys.argv[10]
PUBCNT_ECI_PLOT = sys.argv[11]


def get_labellist(data, xcol, ycol, prelist):
    results = sm.OLS(data[ycol], sm.add_constant(data[xcol]),missing="drop").fit()
    metadata["resid"] = results.resid
    head = data.sort_values(by=['resid'],ascending=False).head(5).Code.tolist()
    tail = data.sort_values(by=['resid'],ascending=True).head(5).Code.tolist()
    labellist = head+tail+prelist
    return labellist

def SetNodeColor(data, naturelist, keilist):
    data['NodeColor'] = "#606060"
    data = data.set_index(keys="Code")
    for item in naturelist:
        data.at[item, 'NodeColor']="#606060"
    for item in keilist:
        data.at[item,'NodeColor']="#606060"
    data = data.reset_index()
    return data

def plot_corr(data, xcol, ycol, ax, labellist, offset):
    """plot correlation between xcol and ycol, label their pcc value
    """
    ax = sns.regplot(x=xcol, y=ycol, data=data, ax=ax, scatter=False,
    line_kws={"linewidth":0.8},truncate=False)
    adjusttext=[]
    for x, y, code, color in zip(data[xcol], data[ycol], data.Code, data.NodeColor):
        ax.scatter(x,y,s = 9,c=color)
        if code in labellist and not np.isnan(x) and not np.isnan(y):
            adjusttext.append(ax.text(x,y,code))
            #ax.text(x+offset,y,code, horizontalalignment='right',verticalalignment='top')
    adjust_text(adjusttext, force_text=0.02,
               arrowprops=dict(arrowstyle="-", color='dimgray', lw=0.5), fontsize="small")
    xvalue=data[xcol].values
    yvalue=data[ycol].values
    nas=np.logical_or(np.isnan(xvalue),np.isnan(yvalue))
    pcc = np.around(np.corrcoef(xvalue[~nas], yvalue[~nas])[0,1],decimals=2)
    #pcc_filter = np.around(np.corrcoef(data_filter[xcol], data_filter[ycol])[0,1],decimals=2)
    #pcc_all = '{}({})'.format(pcc,pcc_filter)
    text = '{}={}'.format("PCC", pcc)
    plt.text(0.05, 0.9,text, transform = ax.transAxes, fontsize=17)
    ax.tick_params(labelsize=16)
    return ax

start_year, end_year = nsp.core.extract_years_from_path(GINI_FILE_PATH)
period=str(start_year)+"-"+str(end_year)

gini_df = pd.read_csv(GINI_FILE_PATH)
eci_df = pd.read_csv(ECI_FILE_PATH)
income_df = pd.read_csv(INCOME_FILE_PATH)
flag_table = pd.read_csv(FLAG_TABLE_PATH, sep="\t")
pub_cnt = pd.read_csv(PUBCNT_PATH)

gini_df = gini_df.merge(right=flag_table, left_on="COUNTRY", right_on="WoS")
eci_df = eci_df[["Year", "Country", "ECI"]]
eci_df = pd.pivot_table(eci_df, index=[
    "Country"], columns='Year', values="ECI").reset_index().rename_axis(None, axis=1)

eci_df["ECI_AVG"] = eci_df[[ind for ind in np.arange(
    start_year, end_year+1)]].mean(axis=1)
eci_df = eci_df[["Country", "ECI_AVG"]].merge(
    right=flag_table, left_on="Country", right_on="ECI_Country")

income_df=income_df[income_df.Year==period]
income_df = income_df.dropna()
income_df['log_income']=np.log10(income_df['Income'])

pub_cnt=pub_cnt[pub_cnt['YEAR'].between(int(start_year),int(end_year))]
pub_cnt=pub_cnt.groupby(['COUNTRY'])['PAPER_CNT'].sum().reset_index()


metadata = gini_df.merge(right=eci_df, how="left",
                        left_on="Code", right_on="Code")
metadata = metadata.merge(right=income_df, how="left",on="Code")
metadata = metadata.merge(pub_cnt,left_on='COUNTRY',right_on='COUNTRY',how='left')
metadata['PAPER_CNT'] = metadata['PAPER_CNT']/5


metadata = metadata[["COUNTRY", "GINI", "Code", "ECI_AVG", "log_income","PAPER_CNT"]]
#metadata = metadata.dropna(axis=0)
metadata = metadata.reset_index(drop=True)

#use 1-gini to represent diversity
metadata['DIVERSITY'] = 1-metadata['GINI']
metadata['PAPER_CNT']=np.log10(metadata['PAPER_CNT'])

naturelist=['NOR','OMN','QAT','SAU','TTO','ARE']
keilist=['AUS','CAN','DNK','FIN','NLD','SWE','CHE','GBR','USA']
metadata = SetNodeColor(metadata, naturelist, keilist)




mpl.rcParams['axes.linewidth'] = 0.6 #set the value globally

prelist = ['USA', 'CHN','GBR','FRA','CAN','AUT','ARE','QAT','KWT',
          'CHE','KOR','IND','SGP','RUS','ZAF','JPN','IRN','GIN','PNG',
          'TKM','GAB','PAN','MUS','TTO','ETH','MOZ','LBN','SRB','SAU',
          'OMN','GRC','PRT','IRL','AUS','DNK','FIN','NLD','BGD','NGA','SDN',
          'SVK','UKR ']
fig,ax = plt.subplots()
plt.xlim(0,1.0005)
ax = plot_corr(metadata, "DIVERSITY", "ECI_AVG", ax, prelist,0.005)
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
plt.xlabel("Scientific diversity", fontsize=19)
plt.ylabel("ECI", fontsize=19)
plt.savefig(GINI_ECI_PLOT, format="pdf", bbox_inches='tight')


prelist = ['USA', 'CHN','GBR','FRA','CAN','AUT','ARE','QAT','KWT',
          'CHE','KOR','IND','SGP','RUS','ZAF','JPN','IRN',
          'TKM','GAB','PAN','MUS','TTO','ETH','MOZ','LBN','SRB','SAU',
          'OMN','GRC','PRT','IRL','AUS','DNK','FIN','NLD']
fig,ax = plt.subplots()
plt.xlim(0,1.0005)
ax = plot_corr(metadata, "DIVERSITY", "log_income", ax, prelist,0.005)
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
#yfmt = ScalarFormatter()
#yfmt.set_powerlimits((0,4))
#plt.gca().yaxis.set_major_formatter(yfmt)
#plt.gca().set_ylim(bottom=-10000)
plt.xlabel("Scientific diversity", fontsize=19)
plt.ylabel(r'log$_{10}$(GDP)', fontsize=19)
plt.savefig(GINI_INCOME_PLOT, format="pdf", bbox_inches='tight')

fig,ax=plt.subplots()
xmin=np.floor(metadata.dropna(subset=['PAPER_CNT','DIVERSITY'])['PAPER_CNT'].min())
ymin=np.floor(metadata.dropna(subset=['PAPER_CNT','DIVERSITY'])['DIVERSITY'].min())
plt.ylim(ymin,1.0005)
plt.xlim(xmin,7)
ax = plot_corr(metadata, "PAPER_CNT", "DIVERSITY",  ax, prelist,0.005)
plt.yticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
plt.xlabel(r'log$_{10}$(Number of Publication)', fontsize=19)
plt.ylabel("Scientific diversity", fontsize=19)
plt.savefig(PUBCNT_GINI_PLOT, format="pdf", bbox_inches='tight')


fig,ax=plt.subplots()
xmin=np.floor(metadata.dropna(subset=['PAPER_CNT','log_income'])['PAPER_CNT'].min())
ymin=np.floor(metadata.dropna(subset=['PAPER_CNT','log_income'])['log_income'].min())
plt.xlim(xmin,7)
plt.ylim(ymin,14)
ax = plot_corr(metadata, "PAPER_CNT","log_income",  ax, prelist,0.005)
plt.xlabel(r'log$_{10}$(Number of Publication)', fontsize=19)
plt.ylabel(r'log$_{10}$(GDP)', fontsize=19)
plt.savefig(PUBCNT_INCOME_PLOT, format="pdf", bbox_inches='tight')


prelist = ['USA', 'CHN','GBR','FRA','CAN','AUT','ARE','QAT','KWT',
          'CHE','KOR','IND','SGP','RUS','ZAF','JPN','IRN',
          'GAB','MUS','LBN','SRB','SAU',
          'OMN','GRC','PRT','IRL','AUS','DNK','FIN','NLD']
fig,ax=plt.subplots()
xmin=np.floor(metadata.dropna(subset=['PAPER_CNT','ECI_AVG'])['PAPER_CNT'].min())
ymin=np.floor(metadata.dropna(subset=['PAPER_CNT','ECI_AVG'])['ECI_AVG'].min())
ymax=np.floor(metadata.dropna(subset=['PAPER_CNT','ECI_AVG'])['ECI_AVG'].max())
plt.xlim(xmin,7)
plt.ylim(ymin,ymax)
ax = plot_corr(metadata, "PAPER_CNT","ECI_AVG",  ax, prelist,0.005)
plt.xlabel(r'log$_{10}$(Number of Publication)', fontsize=19)
plt.ylabel('ECI', fontsize=19)
plt.savefig(PUBCNT_ECI_PLOT, format="pdf", bbox_inches='tight')


prelist = ['USA', 'CHN','GBR','FRA','CAN','AUT','ARE','QAT','KWT',
          'CHE','KOR','IND','SGP','RUS','ZAF','JPN','IRN','GIN','PNG',
          'TKM','GAB','PAN','MUS','TTO','ETH','MOZ','LBN','SRB','SAU','OMN','GRC','PRT','IRL','AUS','DNK','FIN','NLD']
fig,ax = plt.subplots()
labellist = get_labellist(metadata, "ECI_AVG", "log_income", prelist)
ax = plot_corr(metadata, "ECI_AVG", "log_income", ax, labellist,0.01)
#yfmt = ScalarFormatter()
#yfmt.set_powerlimits((0,4))
#plt.gca().yaxis.set_major_formatter(yfmt)
#plt.gca().set_ylim(bottom=-10000)
plt.xlabel("ECI", fontsize=19)
plt.ylabel(r'log$_{10}$(GDP)', fontsize=19)
plt.savefig(INCOME_ECI_PLOT, format="pdf", bbox_inches='tight')
