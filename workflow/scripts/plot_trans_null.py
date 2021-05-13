import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

NULL_TRANS_FILE = sys.argv[1]
CNTRY_GROUP_FILE = sys.argv[2]
PLOT_PATH = sys.argv[3]

null_trans = pd.read_csv(NULL_TRANS_FILE)
cntry_group = pd.read_csv(CNTRY_GROUP_FILE)

null_trans = null_trans.merge(cntry_group, left_on=['COUNTRY','PERIOD'], right_on=['COUNTRY','YEAR'])

fig, axs = plt.subplots(1,3, figsize=(15,6))
plot_order=['NM','NE','SHM']
hue_order=['exp','actual']
for ind, group in enumerate(plot_order):
    group_df = null_trans[null_trans.GROUP_ADV == group]
    sns.boxplot(x='DIS_GROUP', y='NUM_CHANGE', hue='SOURCE', data=group_df, 
    ax=axs[ind], hue_order=hue_order)
    axs[ind].set_title(group)
plt.savefig(PLOT_PATH, format="pdf",bbox_inches="tight")