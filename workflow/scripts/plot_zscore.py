import seaborn as sns
import matplotlib.pyplot as plt
import pandas as import pd
import sys

ZSCORE_FILE_PATH = sys.argv[1]
PLOT_PATH = sys.argv[2]

zscore_df = pd.read_csv(ZSCORE_FILE_PATH)
zscore_df = zscore_df.melt(id_vars="YEAR",var_name="MEASURE",value_name="zscore")

fig, ax = plt.subplots()
sns.set(style="ticks", rc={"lines.linewidth": 1})
sns.pointplot(x='YEAR',y='zscore',hue='MEASURE',data=zscore_df,ax=ax)
ax.tick_params(axis="x",labelrotation=45)
ax.set_ylabel(ylabel="ZSCORE", fontsize='large')
ax.set_xlabel(xlabel="YEAR", fontsize='large')
ax.axhline(0, ls='--')
plt.savefig(PLOT_PATH,format="pdf",bbox_inches="tight")
