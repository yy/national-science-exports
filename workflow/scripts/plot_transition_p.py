import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import copy
import sys
from matplotlib.lines import Line2D
from scipy import stats

def plot_bar_transition(plot_df, xcol, ycol, xlabel, ylabel):
    x = plot_df[xcol].values.tolist()
    y = plot_df[ycol].values

    fig, ax = plt.subplots()
    plt.bar(x,y,alpha=0.5,ecolor='black',width=0.045)
    plt.xlabel(xlabel, fontsize=19)
    plt.ylabel(ylabel, fontsize=19)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    return fig, ax

def cal_bin_prob(filtered_df):
    filtered_df = filtered_df.groupby(['binned', 'st1']).size().reset_index(name='num')
    filtered_df = filtered_df.pivot(index='binned', columns='st1', values='num')
    filtered_df.columns=['fail','suc']
    filtered_df = filtered_df.div(filtered_df.sum(axis=1), axis=0).reset_index()
    filtered_df['binned'] = filtered_df['binned'].astype('float')
    filtered_df = filtered_df.fillna(value=0)
    return filtered_df

def plot_distribution(density_df):
    fig, ax = plt.subplots()
    x1 = density_df[density_df.st1 ==1]["Density"].values
    x2 = density_df[density_df.st1 ==0]["Density"].values
    sns.kdeplot(x1, ax=ax, color="#3498db")
    sns.kdeplot(x2, ax=ax, color="r")
    lines = [Line2D([0], [0], color="#3498db", label="Activation"),
    Line2D([0], [0], color="r", label="Inactivation")]
    plt.legend(handles = lines, frameon=False, fontsize='medium')
    plt.xlabel("Neighbors\' Density", fontsize=19)
    plt.ylabel("Kernal Density", fontsize=19)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    return fig, ax




DENSITY_FILE_PATH = sys.argv[1]
ACTIVATION_PLOT = sys.argv[2]
INACTIVATION_PLOT = sys.argv[3]
ACT_INACT_DISTRIBUTION_PLOT = sys.argv[4]
#PARAMS_FILE_OUTPUT = sys.argv[5]


density_df = pd.read_csv(DENSITY_FILE_PATH)
density_df = density_df[density_df.DIS != "Unknown"]

bins = np.arange(0,1.05,0.05)
labels=labels = np.arange(0.05,1.05,0.05)
density_df['binned'] = pd.cut(density_df['Density'], bins, labels = labels,include_lowest=True)

params_df = pd.DataFrame(index=['activation', 'inactivation'], columns=['intercept','slope'])

activate_df = density_df[density_df.st0==0]
activate_df = cal_bin_prob(activate_df)
fig, ax = plot_bar_transition(
    activate_df, 'binned', 'suc', 'Neighbors\' Density','Probability of activation')
plt.savefig(ACTIVATION_PLOT, format="pdf", bbox_inches="tight")
x = activate_df['binned'].values.tolist()
y = activate_df['suc'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
params_df.at['activation','intercept'] = intercept
params_df.at['activation','slope'] = slope

inact_df = density_df[density_df.st0==1]
inact_df = cal_bin_prob(inact_df)
fig, ax = plot_bar_transition(
    inact_df, 'binned','fail','Neighbors\' Density','Probability of inactivation'
)
plt.savefig(INACTIVATION_PLOT, format="pdf", bbox_inches="tight")
x = inact_df['binned'].values.tolist()
y = inact_df['fail'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
params_df.at['inactivation','intercept'] = intercept
params_df.at['inactivation','slope'] = slope

fig, ax = plot_distribution(density_df)
plt.savefig(ACT_INACT_DISTRIBUTION_PLOT, format="pdf", bbox_inches="tight")

#params_df.to_csv(PARAMS_FILE_OUTPUT)
