import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib


CNTRY_GROUP=sys.argv[1]
GDPFILE=sys.argv[2]
FLAG_TABLE = sys.argv[3]
OUTPUT=sys.argv[4]

cntry_grp=pd.read_csv(CNTRY_GROUP)
gdp=pd.read_csv(GDPFILE)
flag_df=pd.read_csv(FLAG_TABLE,sep="\t")

cntry_meta=cntry_grp.merge(flag_df[['WoS','Code']],left_on='COUNTRY',right_on='WoS')
cntry_meta=cntry_meta.merge(gdp, left_on=['Code','YEAR'],right_on=['Code','Year'])
cntry_meta = cntry_meta[['WoS','Code','Year','GROUP_ADV','Income']]
cntry_meta=cntry_meta.dropna()
cntry_meta=cntry_meta.replace({'GROUP_ADV':{'SHM':'S','NE':'P','NM':'N'}})

cntry_grp_initial=cntry_meta.query('Year=="1973-1977"')[['Code','GROUP_ADV','Income']]
cntry_grp_initial.columns=['country','group_init','income_init']
cntry_grp_recent=cntry_meta.query('Year=="2013-2017"')[['Code','GROUP_ADV','Income']]
cntry_grp_recent.columns=['country','group_recent','income_recent']
cntry_grp_meta = cntry_grp_initial.merge(cntry_grp_recent,on='country',how='inner')


cntry_grp_meta = cntry_grp_meta.dropna()
cntry_grp_meta['gdp_growth']=np.log10((cntry_grp_meta['income_recent'])/(cntry_grp_meta['income_init']))
cntry_grp_meta['label']=cntry_grp_meta['group_init']+str("-")+cntry_grp_meta['group_recent']
cntry_grp_meta['income_recent_log']=np.log10(cntry_grp_meta['income_recent'])



sum_df = cntry_grp_meta.groupby('label').agg({'country':'count','gdp_growth':'mean'}).sort_values(by='gdp_growth')
sum_df=sum_df.reset_index()




xs=np.arange(0,sum_df.shape[0])-0.2
ys=[0.6 for x in range(sum_df.shape[0])]
fig, ax=plt.subplots()
order=sum_df.label.tolist()
text=sum_df.country.tolist()
text=['('+str(a)+')' for a in text]
cmap=cm.get_cmap('viridis')
# Normalize to the range of possible values from df["c"]
norm = matplotlib.colors.Normalize(vmin=cntry_grp_meta['income_recent_log'].min(), vmax=cntry_grp_meta['income_recent_log'].max())
# create a color dictionary (value in c : color from colormap)
colors = {}
for cval in cntry_grp_meta['income_recent_log']:
    colors.update({cval : cmap(norm(cval))})
sns.boxplot(x='label',y='gdp_growth',data=cntry_grp_meta,order=order,ax=ax, width=0.2,color="darkgrey",linewidth=0.2)
sns.swarmplot(x="label", y="gdp_growth", data=cntry_grp_meta, ax=ax,order=order,
             hue='income_recent_log',palette=colors)
for i,box in enumerate(ax.artists):
    box.set_edgecolor('black')
    box.set_facecolor('white')
for ind, s in enumerate(text):
    plt.text(xs[ind],ys[ind],s)
plt.xticks(rotation="45")
plt.gca().legend_.remove()
plt.ylabel("log$_{10}$GDP growth", fontsize=15)
plt.xlabel("Cluster transition", fontsize=15)


divider = make_axes_locatable(plt.gca())
ax_cb = divider.new_horizontal(size="5%", pad=0.15)
fig.add_axes(ax_cb)
cb1 = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=cmap,
                                norm=norm,
                                orientation='vertical')

plt.savefig(OUTPUT,bbox_inches='tight')
