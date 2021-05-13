import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

RAW_GINI=sys.argv[1]
NORM_GINI=sys.argv[2]
PLOT_FILE=sys.argv[3]

rawgini=pd.read_csv(RAW_GINI)
normgini=pd.read_csv(NORM_GINI)
normgini=normgini.rename({'GINI','GININORM'},axis='columns')
gini_meta=rawgini.merge(normgini,on=['COUNTRY','YEAR'],how='inner')

fig,ax=plt.subplots()
sns.scatterplot(data=gini_meta,x='GININORM',y='GINI',ax=ax)
pcc=np.around(np.corrcoef(gini_meta['GININORM'],gini_meta['GINI'])[0,1],decimals=2)
text = '{}={}'.format("PCC", pcc)
plt.text(0.05, 0.9,text, transform = ax.transAxes, fontsize=17)
ax.tick_params(labelsize=16)
plt.xticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
plt.yticks(np.arange(0,11,2)/10,np.arange(0,11,2)/10)
plt.xlabel('Normalized GINI',fontsize=18)
plt.ylabel('Raw GINI',fontsize=18)
plt.savefig(PLOT_FILE, format="pdf", bbox_inches='tight')
