import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

TERCHANGE_FILE=sys.argv[1]
RESOURCE_CHANGE_PLOT=sys.argv[2]
APPLIED_CHANGE_PLOT=sys.argv[3]
SOCIAL_CHANGE_PLOT=sys.argv[4]

def get_position(data, labellist,colname):
    label_df = data[data.country.isin(labellist)].set_index("country")
    label_df = label_df.reindex(labellist)
    xlist=label_df[colname].tolist()
    ylist=label_df.growth_log.tolist()
    return xlist, ylist

def plot_change(data, xcol,xlabel,labellist, xlist,ylist):

    xvalue=data[xcol].values
    yvalue=data['growth_log'].values
    cvalue=data['income_2013_log'].values

    fig, ax=plt.subplots(figsize=(8,5))
    point = ax.scatter(xvalue,yvalue,c=cvalue,cmap="viridis",s=20)
    for ind, label in enumerate(labellist):
        x = xlist[ind]
        y = ylist[ind]
        plt.text(x,y,label)
    pcc = np.around(np.corrcoef(xvalue, yvalue)[0,1],decimals=2)
    text = '{}={}'.format("PCC", pcc)
    plt.text(0.70, 0.85,text, transform = ax.transAxes, fontsize=17)
    #plt.ylim(-1,72)
    plt.vlines(0,0,5,linestyle="--",color="grey")
    fig.colorbar(point)
    ax.tick_params(axis='both', labelsize=10)
    plt.xlim(-0.8,0.8)
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel("log GDP Growth", fontsize=15)
    return fig, ax

ter_df=pd.read_csv(TERCHANGE_FILE)

nmlist=['KHM','QAT','CHN','SGP','CYP','KOR','BOL','BEN','LIE','OMN','VCT','TON']
xlist, ylist=get_position(ter_df,nmlist, 'nm_change')
fig, ax=plot_change(ter_df, 'nm_change','Increase in Resource',nmlist, xlist, ylist)
plt.savefig(RESOURCE_CHANGE_PLOT, bbox_inches='tight')

nelist=['MYS','SGP','KOR','DZA','CHN','KHM','QAT','CYP','BWA','MUS','OMN','ARE',
          'IRL','JAM','ZWE','CAF','MAR','IRN','TUN','GAB','NLD','LIE']
xlist, ylist=get_position(ter_df, nelist, 'ne_change')
fig, ax=plot_change(ter_df,'ne_change','Increase in Applied', nelist, xlist, ylist)
plt.savefig(APPLIED_CHANGE_PLOT, bbox_inches='tight')

shmlist=['KHM','QAT','CHN','SGP','CYP','TON','VCT','LIE','MCO','GBR','MEX','TUN','PAN']
xlist, ylist=get_position(ter_df, shmlist, 'shm_change')
fig, ax=plot_change(ter_df,'shm_change','Increase in Societal', shmlist, xlist, ylist)
plt.savefig(SOCIAL_CHANGE_PLOT, bbox_inches='tight')
