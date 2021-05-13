""" This script plots the nestedness

input:
- argv[1]: the rca matrix

output:
- argv[2]: the nestedness figure

"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import numpy as np
from matplotlib.colors import ListedColormap
import sys
import os
import nsp.core


def plot_nest(ordered_rca_df, ax):
    mpl.rcParams['axes.linewidth'] = 0.6 #set the value globally

#    cmap = colors.ListedColormap(["white", "black"])
#    upperbounds = ordered_rca_df.max().max()
#    bounds = [0, 1, upperbounds]
#    norm = colors.BoundaryNorm(bounds, cmap.N)
#    sns.heatmap(np.array(ordered_rca_df), cmap=cmap, norm=norm, ax=ax, cbar=False)

    col_dict={0:"#FFFFFF",
              1:"#E8C434",
              2:"#E4C2F2",
              3:"#B3E0F2"}
    cm = ListedColormap([col_dict[x] for x in col_dict.keys()])
    sns.heatmap(np.array(ordered_rca_df), cmap=cm,cbar=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel("Countries", fontsize=19)
    ax.set_xlabel("Disciplines", fontsize=19)

    return ax


if __name__ == "__main__":
    RCA_FILE = sys.argv[1]
    DSCP_FILE = sys.argv[2]
    PLOT_FILE = sys.argv[3]
    NESTED_MATRIX_FILE = sys.argv[4]
    #print(DSCP_FILE)
    print(PLOT_FILE)
    print(NESTED_MATRIX_FILE)

    rca_df = pd.read_csv(RCA_FILE).set_index("COUNTRY")
    rca_df = nsp.core.order_rca_matrix(rca_df, False, False)


    rca_df[rca_df>1]=1
    rca_df[rca_df<1]=0
    dscp_grp = pd.read_csv(DSCP_FILE, sep="\t", names=['DIS','GROUP'])
    grouplist = ['NM','NE','SHM']
    dscp_grp["GROUP"] = pd.Categorical(dscp_grp["GROUP"], categories=grouplist, ordered=True)
    dscp_grp = dscp_grp[dscp_grp.DIS != "Unknown"]
    dscp_grp.sort_values('GROUP', inplace=True)
    for index, group in enumerate(grouplist):
        dscplist = dscp_grp[dscp_grp.GROUP==group].DIS.tolist()
        rca_df[dscplist] = rca_df[dscplist].replace(1,index+1)

    mpl.rcParams['axes.linewidth'] = 0.6
    f, ax = plt.subplots(figsize=(6,7))
    ax = plot_nest(rca_df, ax)
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(0.6)
        spine.set_edgecolor('#A6A6A6')
    #print(PLOT_FILE)
    plt.savefig(PLOT_FILE)

    rca_df[rca_df>1] = 1
    rca_df[rca_df<1] = 0
    rca_df.to_csv(NESTED_MATRIX_FILE, header=False, index=False)
