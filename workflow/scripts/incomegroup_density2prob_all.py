import sys
import itertools
from os.path import join as pjoin
from functools import partial

import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from itertools import product
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)

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
binsize=0.05
bins = np.arange(0, 1.05, binsize)
labels = labels = np.arange(0.05, 1.05, 0.05)
density_df["binned"] = pd.cut(
    density_df["Density"], bins, labels=labels, include_lowest=True
)
density_df = density_df[density_df.DIS != "Unknown"]

def resample_transition(df, incomegroup="ALL", from_st=0, threshold_cnt=20):
    if incomegroup != "ALL":
        df = df.query(f"INCOMEGROUP == '{incomegroup}'")
    cnt_df = df.loc[:, ["st0", "st1", "binned"]].sample(
        len(df), replace=True
    ).query(f"st0 == {from_st}").groupby(
        ["binned", "st1"]
    ).size().reset_index(name="count").pivot(index="binned", columns="st1", values="count")
    cnt_df = cnt_df[cnt_df[0] + cnt_df[1] > threshold_cnt]
    return cnt_df.div(cnt_df.sum(axis=1), axis=0).dropna()  # if fillna(0) is used, then it will throw out data points.


def ols_beta(df, end_state):
    sm_df = df.rename(columns={end_state: "TARGET"}).reset_index()
    sm_df['x'] = sm_df.binned.astype('float')
    sm_df['x']=sm_df['x']-(binsize/2)
    result = smf.ols("TARGET ~ x", data=sm_df).fit()
    return (result.params[0], result.params[1])

plot_data = {}
income_group = ["L", "LM", "UM", "H"]
starting_states = [0, 1] # 0: DISADV, 1: ADV
N_ENSEMBLES=20
for igroup, st_state in product(income_group + ["ALL"], starting_states):
    end_state = 0 if st_state else 1
    print(igroup, st_state, end_state)

    plot_data[(igroup, st_state)] = {'x': [], 'y': [], 'beta': [], 'beta0': []}

    for i in range(N_ENSEMBLES):
        df = resample_transition(density_df, incomegroup=igroup, from_st=st_state)
        plot_data[(igroup, st_state)]['x'].append(np.array(df.index))
        plot_data[(igroup, st_state)]['y'].append(np.array(df[end_state]))

        beta0, beta = ols_beta(df, end_state=end_state)
        plot_data[(igroup, st_state)]['beta0'].append(beta0)
        plot_data[(igroup, st_state)]['beta'].append(beta)

pd.DataFrame(
    (igroup, st_state, np.mean(curr_data['beta0']), np.mean(curr_data['beta']))
        for (igroup, st_state), curr_data in plot_data.items()
).rename(
    columns={0: "INCOME_GROUP", 1: "START_STATE", 2: "CONSTANT", 3: "SLOPE"}
).to_csv(PARAMS_RESULT, index=False)

colormap = {"L": "#1B65A6", "LM": "#9BDAF2", "UM": "#FFAF4D", "H": "#E05E00", "ALL": "#008F00"}
scatter_size = 0.2
linewidth = 0.5

def plot_transition(ax, data, igroups=["ALL"], st_state=0):
    ylabel = {0: "Activation probability", 1: "Deactivation probability"}
    ax.set_xlim((0.0, 0.82))
    ax.set_ylim((0.0, 1.02))
    ax.set_ylabel(ylabel[st_state], fontsize=12)

    for igroup in igroups:
        ind_data = data[(igroup, st_state)]
        x_all = list(itertools.chain(*ind_data['x']))
        y_all = list(itertools.chain(*ind_data['y']))
        beta_mean, beta_std = np.mean(ind_data['beta']), np.std(ind_data['beta'])
        for sample_idx in range(N_ENSEMBLES):
            ax.scatter(x=add_jitter(ind_data['x'][sample_idx], 0.025),y=ind_data['y'][sample_idx],
                       s=scatter_size, c=colormap[igroup])
        sns.regplot(x=x_all, y=y_all, scatter=False, ci=99, ax=ax, color=colormap[igroup],
                    line_kws={"linewidth": linewidth},
                    label=f"{igroup}, Slope: {beta_mean:.2f} ({beta_std:.2f})")
    return fig, ax

def add_jitter(data, jitter_width=1.0):
    return data + (np.random.sample(size=len(data)) - 0.5) * jitter_width
fig, axs = plt.subplots(2, 2, sharex=True, sharey=False, figsize=(8,5))

plot_transition(ax=axs[0][0], data=plot_data, igroups=["ALL"], st_state=0)
plot_transition(ax=axs[0][1], data=plot_data, igroups=["ALL"], st_state=1)
plot_transition(ax=axs[1][0], data=plot_data, igroups=income_group, st_state=0)
plot_transition(ax=axs[1][1], data=plot_data, igroups=income_group, st_state=1)

plt.subplots_adjust(wspace=0.05)

axs[1][0].set_xlabel("Density", fontsize=14)
axs[1][1].set_xlabel("Density", fontsize=14)

axs[0][0].legend(loc="upper left", frameon=False)
axs[0][1].legend(loc="upper right", frameon=False)
axs[1][0].legend(loc="upper left", frameon=False)
axs[1][1].legend(loc="upper right", frameon=False)


fig.tight_layout()
fig.savefig(DENSITY_PLOT_PATH)
