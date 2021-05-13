"""plot the comparision between resampled gini and actual raw gini
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
import sys
import nsp.core

GINI_ACTUAL_PATH = sys.argv[1]
GINI_SAMPLED_PATH = sys.argv[2]
INCOME_FILE = sys.argv[3]
PLOT_OUTPUT_PATH = sys.argv[4]

gini_actual_df = pd.read_csv(GINI_ACTUAL_PATH)
gini_sampled_df = pd.read_csv(GINI_SAMPLED_PATH)
gini_sampled_df.columns=['COUNTRY','boot','YEAR']
income_df = pd.read_csv(INCOME_FILE)

gini_meta=gini_actual_df.merge(gini_sampled_df,on=['COUNTRY','YEAR'],how='inner')
gini_meta=gini_meta.merge(income_df,left_on=['COUNTRY','YEAR'],right_on=['WoS','YEAR'],how='inner')
#plot
st_order = ["L","LM",'UM','H']
hue_order = ["1988-1992","1993-1997", "1998-2002", "2003-2007", "2008-2012", "2013-2017"]

gini_meta['GINI']=1-gini_meta['GINI']
gini_meta['boot']=1-gini_meta['boot']

mpl.rcParams['axes.linewidth'] = 0.6
fig,ax = plt.subplots(figsize=[8,6])
sns.pointplot(x="GINI", y="IncomeGroup", data=gini_meta, join=False, order=st_order, hue="YEAR", ci="sd",
              palette="Blues", hue_order=hue_order, dodge=0.5, errwidth=1.2, scale=0.8, ax=ax)
sns.pointplot(x="boot", y="IncomeGroup", data=gini_meta, join=False, order=st_order, hue="YEAR", ci="sd",
              palette="gray_r", hue_order=hue_order, dodge=0.5, errwidth=1.2, scale=0.8, ax=ax)
ax.tick_params(labelsize=15)

handles, labels = ax.get_legend_handles_labels()
#add to extra handles and labels for legend
legend_elements = [Line2D([0], [0], marker='o', color='#4D4F53',
                          markerfacecolor='#4D4F53', markersize=5),
                  Line2D([0], [0], marker='o', color='#186BD9',
                          markerfacecolor='#186BD9', markersize=5)]
legend_labels=["Sampled","Actual"]
handles[0:0] = legend_elements
labels[0:0] = legend_labels
#remove the redandunt legends
handles = handles[0:8]
labels = labels[0:8]
ax.legend(handles=handles, labels=labels, loc=4, frameon=False, fontsize=12)

ax.text(0.3,0.1, "Low", fontsize=15)
ax.text(0.38,1.1, "Low-Middle", fontsize=15)
ax.text(0.4,2.1, "Upper-Middle", fontsize=15)
ax.text(0.52,3.1, "High", fontsize=15)
ax.set_yticklabels([])
ax.set_yticks([])
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)

plt.xlabel("Scientific Diversity", fontsize=19)
plt.ylabel("Income Classification", fontsize=19)

plt.savefig(PLOT_OUTPUT_PATH, format="pdf", bbox_inches="tight")
