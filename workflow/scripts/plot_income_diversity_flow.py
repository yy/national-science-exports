import itertools
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

GINI_FILE = sys.argv[1]
INCOME_FILE = sys.argv[2]
FLAG_TABLE = sys.argv[3]
YEAR_INTERVAL = sys.argv[4]
PLOT_FILE = sys.argv[5]

gini_df = pd.read_csv(GINI_FILE)
income_df = pd.read_csv(INCOME_FILE)
flag_table = pd.read_csv(FLAG_TABLE, sep="\t")
with open(YEAR_INTERVAL) as f:
    yearorder = f.read().splitlines()

gini_df = gini_df.merge(flag_table[["WoS", "Code"]], left_on="COUNTRY", right_on="WoS")
income_df = income_df.rename(columns={"Year": "YEAR"})
metadata = gini_df[["Code", "GINI", "YEAR", "ST"]].merge(income_df, on=["Code", "YEAR"])
metadata["Diversity"] = 1 - metadata["GINI"]
metadata["log_gdp"] = np.log10(metadata["Income"])
metadata = metadata.dropna()

maxvalue = np.ceil(metadata.log_gdp.max())
minvalue = np.floor(metadata.log_gdp.min())
ybins = np.arange(minvalue, maxvalue, 0.5)
ylabels = np.arange(minvalue + 0.5, 14, 0.5)
xbins = np.arange(0, 10, 1) / 10
xlabels = np.arange(1, 10, 1) / 10

metadata["ybins"] = pd.cut(metadata["log_gdp"], bins=ybins, labels=ylabels)
metadata["xbins"] = pd.cut(metadata["Diversity"], bins=xbins, labels=xlabels)

x_start = []
y_start = []
x_end = []
y_end = []
for xgrid, ygrid in itertools.product(xlabels, ylabels):
    cell_df = metadata[(metadata.xbins == xgrid) & (metadata.ybins == ygrid)]
    cell_df = cell_df[cell_df.YEAR != "2013-2017"]
    current_df = pd.DataFrame()
    next_df = pd.DataFrame()
    for index, row in cell_df.iterrows():
        cntry_code = row["Code"]
        year_crrt = row["YEAR"]
        year_next_index = yearorder.index(year_crrt) + 1
        cntry_next = metadata[
            (metadata.Code == cntry_code)
            & (metadata.YEAR == yearorder[year_next_index])
        ]
        if not cntry_next.empty:
            current_df = pd.concat([current_df, cell_df.loc[[index]]])
            next_df = pd.concat([next_df, cntry_next])
    if not current_df.empty:
        x_start.append(current_df.Diversity.mean())
        y_start.append(np.log10(current_df.Income.mean()))

        x_end.append(next_df.Diversity.mean())
        y_end.append(np.log10(next_df.Income.mean()))

fig, ax = plt.subplots()

for index, value in enumerate(x_start):
    ax.annotate(
        text="",
        xy=(x_end[index], y_end[index]),
        xytext=(x_start[index], y_start[index]),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
    )


xvalue=metadata['Diversity'].values
yvalue=metadata['log_gdp'].values
m, b=np.polyfit(xvalue,yvalue,1)
plt.plot(xvalue, m*xvalue + b,'r:', alpha=0.5,linewidth=0.6)
ax.set_yticks(np.arange(6, 14,1), minor=True)
ax.tick_params(labelsize=16)
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
plt.ylim(6,14)
ax.grid(False)
plt.xlabel("Scientific Diversity",fontsize=18)
plt.ylabel(r'log$_{10}$(GDP)',fontsize=18)
plt.savefig(PLOT_FILE,bbox_inches='tight')
