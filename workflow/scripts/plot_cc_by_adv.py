import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

CC_PATH = sys.argv[1]
CNTRY_ST_PATH = sys.argv[2]
PLOT_OUTPUT_PATH = sys.argv[3]

cc_df = pd.read_csv(CC_PATH)
cntry_st = pd.read_csv(CNTRY_ST_PATH,sep="\t", names=['COUNTRY','st'])
cc_df = cc_df.merge(cntry_st, on="COUNTRY")

st_order = ["Advanced", "Proficient", "Developing", "Lagging"]
hue_order = ["1973-1977", "1978-1982", "1983-1987", "1988-1992",
             "1993-1997", "1998-2002", "2003-2007", "2008-2012", "2013-2017"]
fig, ax = plt.subplots()
sns.pointplot(x="MODU", y="st", data=cc_df, join=False, order=st_order, hue="PERIOD",
              palette="Blues", hue_order=hue_order, dodge=0.5, errwidth=1.2, scale=0.8, ax=ax)
#plt.legend(fontsize=11, loc=(1.01,0.310))
ax.legend().set_visible(False)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Scientific specialization",fontsize=17)
plt.ylabel("S&T Classification", fontsize=17)
ax.set_yticklabels([])
ax.set_yticks([])
plt.text(0.22,0.10, "Advanced", fontsize=15)
plt.text(0.23,1.2, "Proficient", fontsize=15)
plt.text(0.24,2.1, "Developing", fontsize=15)
plt.text(0.20,3.2, "Lagging & Others", fontsize=15)
plt.savefig(PLOT_OUTPUT_PATH, format="pdf", bbox_inches="tight")
