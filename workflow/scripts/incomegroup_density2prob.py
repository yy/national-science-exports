import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib.lines import Line2D

import Boot_Adv as bv

DENSITY_FILE = sys.argv[1]
INCOME_GROUP_FILE = sys.argv[2]
DENSITY_PLOT_PATH = sys.argv[3]
PARAM_FILE = sys.argv[4]

density_df = pd.read_csv(DENSITY_FILE)
income_group_df = pd.read_csv(
    INCOME_GROUP_FILE, sep=",", names=["INCOMEGROUP", "YEAR", "COUNTRY"]
)

density_df = density_df.merge(
    income_group_df,
    left_on=["COUNTRY", "CRRT_TIME"],
    right_on=["COUNTRY", "YEAR"],
    how="left",
)
bins = np.arange(0, 1.05, 0.05)
labels = labels = np.arange(0.05, 1.05, 0.05)
density_df["binned"] = pd.cut(
    density_df["Density"], bins, labels=labels, include_lowest=True
)
density_df = density_df[density_df.DIS != "Unknown"]


income_group=['H','UM','LM','L']
income_label=['High','Upper-Middle','Low-Middle','Low']

fig, ax = plt.subplots()
slopelist = []
constantlist = []
cilist = []


x=np.array([0.0,0.2,0.4,0.6,0.8])
colormap=['#B980F2','#E8C434','#9BDAF2','#1B65A6']
for index in range(4):
    density_selected = density_df[density_df.INCOMEGROUP==income_group[index]]
    data_subset = density_selected.loc[:,['st0','st1','binned']].values
    xlist, ylist=bv.bootstrap(data_subset,bv.theta1_coef,0,'suc')
    ax.set_xlim([0,0.81])
    sns.regplot(xlist,ylist,ax=ax,scatter_kws={'s':1},color=colormap[index],
    line_kws={'linewidth':0.8},truncate=False,x_jitter=0.01)



    x2 = sm.add_constant(xlist)
    mod = sm.OLS(ylist, x2)
    res = mod.fit()
    constantlist.append(np.around(res.params[0], 2))
    slopelist.append(np.around(res.params[1], 2))
    cilist.append(np.around(res.conf_int()[1], 2))
param_df = pd.DataFrame(
    {"group": income_group, "constant": constantlist, "slope": slopelist}
)
param_df.to_csv(PARAM_FILE, index=False)
newlabels = []
for ind in np.arange(4):

    slope=slopelist[ind]
    low=cilist[ind][0]
    high=cilist[ind][1]
    s=income_group[ind]+' Slope:'+str(slope)+" (95% CI:"+str(low)+"—"+str(high)+")"

    newlabels.append(s)

custom_lines = [
    Line2D([0], [0], color=colormap[0]),
    Line2D([0], [0], color=colormap[1]),
    Line2D([0], [0], color=colormap[2]),
    Line2D([0], [0], color=colormap[3]),
]
plt.legend(custom_lines, labels=newlabels, frameon=False, fontsize=12)
plt.xlim(0)
plt.ylim(0)
ax.text(0.6, 0.45, "L", fontsize=11)
ax.text(0.55, 0.42, "LM", fontsize=11)
ax.text(0.6, 0.31, "UM", fontsize=11)
ax.text(0.75, 0.29, "H", fontsize=11)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Density", fontsize=16)
plt.ylabel("Activation Probability", fontsize=16)
plt.savefig(DENSITY_PLOT_PATH, format="pdf", bbox_inches="tight")
