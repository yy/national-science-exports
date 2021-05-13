"""
This script plots the temporary gini change over different income groups
The dot represents the mean value for a specific group
The error bar is the CI from bootstrap

input:
-argv[1]: aggerated gini value file contains gini of all countries in the same time period

output:
-argv[2]: path to save the plot
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import numpy as np
import nsp.core

GINI_FILE = sys.argv[1]
INCOMEGROUP_FILE = sys.argv[2]
PLOT_PATH = sys.argv[3]

gini_df = pd.read_csv(GINI_FILE)
incomegroup = pd.read_csv(INCOMEGROUP_FILE)
gini_df=gini_df.merge(incomegroup, left_on=['COUNTRY','YEAR'],
right_on=['WoS','YEAR'])
#merge others with group lagging
#gini_df = nsp.core.merge_others_lagging(gini_df, "ST")
#gini_df.loc[(gini_df.ST=="Others"),"ST"]="Lagging"
st_order = ['H','UM','LM','L']
hue_order = ["1988-1992","1993-1997", "1998-2002", "2003-2007", "2008-2012", "2013-2017"]
gini_df['DIVERSITY']=1-gini_df['GINI']

mpl.rcParams['axes.linewidth'] = 0.6
fig, ax = plt.subplots()
sns.pointplot(x="DIVERSITY", y="IncomeGroup", data=gini_df, join=False, order=st_order, hue="YEAR",
              palette="Blues", hue_order=hue_order, dodge=0.5, errwidth=1.2, scale=0.8, ax=ax)
plt.setp(ax.collections, sizes=[40])
ax.tick_params(labelsize=15)
plt.legend(fontsize=11, frameon=False, loc=(0.695,-0.010))
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
ax.set_yticklabels([])
ax.set_yticks([])
plt.xlabel("Scientific Diversity", fontsize=19)
plt.ylabel("Income Classification", fontsize=19)
plt.text(0.72,0.02, "High", fontsize=15)
plt.text(0.42,0.9, "Upper-Middle", fontsize=15)
plt.text(0.37,1.9, "Low-Middle", fontsize=15)
plt.text(0.20,2.9, "Low", fontsize=15)
plt.savefig(PLOT_PATH, format="pdf", bbox_inches="tight")
