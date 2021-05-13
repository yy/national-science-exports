import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys


NEST_MODU_FILE = sys.argv[1]
NEST_PLOT_PATH = sys.argv[2]
MODU_PLOT_PATH = sys.argv[3]

mpl.rcParams['xtick.major.size'] = 20
sns.set(style="ticks", rc={"lines.linewidth": 0.6})
mpl.rcParams['axes.linewidth'] = 0.6

zscore_df = pd.read_csv(NEST_MODU_FILE)
zscore_df = zscore_df.sort_values(by='year')
df = zscore_df[zscore_df.prop=="nest"]

fig, ax = plt.subplots()


sns.pointplot(x='year',y='zscore',data=df,ax=ax)
ax.tick_params(axis="x",labelrotation=45,labelsize=12,width=0.5)
ax.tick_params(axis="y",width=0.5)
ax.set_ylabel(ylabel="Z-score of Nestedness", fontsize='large')
ax.set_xlabel(xlabel="")
ax.axhline(0, ls='--')
plt.setp(ax.collections, sizes=[20])
plt.xlim(left=-0.2, right=8.2)
plt.savefig(NEST_PLOT_PATH,format="pdf",bbox_inches="tight")


mpl.rcParams['xtick.major.size'] = 20
sns.set(style="ticks", rc={"lines.linewidth": 0.6})
mpl.rcParams['axes.linewidth'] = 0.6
fig, ax = plt.subplots()
df = zscore_df[zscore_df.prop=="modu"]

sns.pointplot(x='year',y='zscore',data=df,ax=ax)
ax.tick_params(axis="x",labelrotation=45,labelsize=12,width=0.5)
ax.tick_params(axis="y",width=0.5)
ax.set_ylabel(ylabel="Z-score of Modularity", fontsize='large')
ax.set_xlabel(xlabel="")
plt.setp(ax.collections, sizes=[20])
plt.xlim(left=-0.1, right=8.2)
plt.ylim(-1)
plt.savefig(MODU_PLOT_PATH, format="pdf",bbox_inches="tight")
