import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import numpy as np
from matplotlib.colors import ListedColormap
import sys
import os

RCA_FILE = sys.argv[1]
DSCP_FILE = sys.argv[2]
CNTRY_GRP_FILE = sys.argv[3]
PLOT_PATH = sys.argv[4]

YEAR = os.path.splitext(os.path.basename(PLOT_PATH))[0].split("_")[3]
def plot_nest(ordered_rca_df):
    mpl.rcParams['axes.linewidth'] = 0.6 #set the value globally

    #cmap = colors.ListedColormap(["white", "black"])
    #upperbounds = ordered_rca_df.max().max()
    #bounds = [0, 1, upperbounds]
    #norm = colors.BoundaryNorm(bounds, cmap.N)
    #sns.heatmap(np.array(ordered_rca_df), cmap=cmap, norm=norm, ax=ax, cbar=False)
    col_dict={0:"#FFFFFF",
              1:"#E8C434",
              2:"#E4C2F2",
              3:"#B3E0F2"}
    cm = ListedColormap([col_dict[x] for x in col_dict.keys()])
    sns.heatmap(np.array(ordered_rca_df), cmap=cm,cbar=False)
    grpcount = dscp_grp.groupby('GROUP').size().reset_index()
    grpcount.columns=['group','count']
    v1=grpcount[grpcount.group=='NM']['count'].values[0]
    v2=grpcount[grpcount.group=='NE']['count'].values[0]
    v2=v2+v1
    ax.vlines([v1,v2],*ax.get_ylim(),colors='#BFBFBF',linestyles="solid", linewidth=0.8)
    ax.set_xticks([])
    ax.set_yticks([])
    #ax.set_ylabel("Countries", fontsize=19)
    #ax.set_xlabel("Disciplines", fontsize=19)
    #return ax

rca_all = pd.read_csv(RCA_FILE)
rca_df = rca_all[rca_all.YEAR==YEAR]
rca_df = rca_df.pivot(index="COUNTRY",columns="DIS", values="VALUES")
rca_df[rca_df>1]=1
rca_df[rca_df<1]=0
dscp_grp = pd.read_csv(DSCP_FILE, sep="\t", names=['DIS','GROUP'])
grouplist = ['NM','NE','SHM']
dscp_grp["GROUP"] = pd.Categorical(dscp_grp["GROUP"], categories=grouplist, ordered=True)
dscp_grp = dscp_grp[dscp_grp.DIS != "Unknown"]
dscp_grp.sort_values('GROUP', inplace=True)
#assign different values to different disciplines for colormap
for index, group in enumerate(grouplist):
    dscplist = dscp_grp[dscp_grp.GROUP==group].DIS.tolist()

    rca_df[dscplist] = rca_df[dscplist].replace(1,index+1)

#get the rca group for each country
cntry_grp = pd.read_csv(CNTRY_GRP_FILE)
cntry_grp["GROUP_ADV"] = pd.Categorical(cntry_grp["GROUP_ADV"], categories=grouplist, ordered=True)
cntry_grp.sort_values('GROUP_ADV', inplace=True)
cntry_grp_filter = cntry_grp[cntry_grp.YEAR==YEAR]

#reorder columns and index
colorder = dscp_grp.DIS.tolist()
indorder = cntry_grp_filter.COUNTRY.tolist()
rca_reorder = rca_df.reindex(indorder)
rca_reorder = rca_reorder[colorder]

mpl.rcParams['axes.linewidth'] = 0.6
f, ax = plt.subplots(figsize=(6,7))
plot_nest(rca_reorder)
for _, spine in ax.spines.items():
    spine.set_visible(True)
    spine.set_edgecolor('#A6A6A6')
    spine.set_linewidth(0.6)
plt.savefig(PLOT_PATH, format="pdf")
