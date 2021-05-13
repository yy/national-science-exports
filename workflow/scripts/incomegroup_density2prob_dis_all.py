import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib.lines import Line2D

import bootstrap_disadv as bdv

DENSITY_FILE = sys.argv[1]
INCOME_GROUP_FILE = sys.argv[2]
DENSITY_PLOT_PATH = sys.argv[3]
PARAMS_RESULT = sys.argv[4]

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


fig, ax = plt.subplots()
slopelist = []
cilist = []
constant = 0
colormap = ["#6BA5F2"]

density_selected = density_df
data_subset = density_selected.loc[:, ["st0", "st1", "binned"]].values
x, y = bdv.bootstrap(data_subset, bdv.theta1_coef)


ax.set_xlim([0,0.81])
sns.regplot(x,y,ax=ax,scatter_kws={'s':1},color=colormap[0],line_kws={'linewidth':0.5},truncate=False,x_jitter=0.01)



x2 = sm.add_constant(x)
mod = sm.OLS(y, x2)
res = mod.fit()
constant = np.around(res.params[0], 2)
slopelist.append(np.around(res.params[1], 2))
cilist.append(np.around(res.conf_int()[1], 2))

pd.DataFrame([[constant, slopelist[0]]], columns=["constant", "slope"]).to_csv(
    PARAMS_RESULT, index=False
)

labels = []

slope = slopelist[0]
low = cilist[0][0]
high = cilist[0][1]
s = "Slope:" + str(slope) + " (95% CI:" + str(low) + "—" + str(high) + ")"
labels.append(s)

custom_lines = [Line2D([0], [0], color=colormap[0])]
plt.legend(custom_lines, labels=labels, frameon=False, fontsize=12)
plt.xlim(0)
plt.ylim(0)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Density", fontsize=16)
plt.ylabel("Deactivation Probability", fontsize=16)
plt.savefig(DENSITY_PLOT_PATH, format="pdf", bbox_inches="tight")
