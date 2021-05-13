import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

NULL_PROB_FILE = sys.argv[1]
DENSITY_FILE = sys.argv[2]
DSCP_FILE = sys.argv[3]
CNTRY_GRP = sys.argv[4]
PLOT_FILE = sys.argv[5]

final_prob=pd.read_csv(NULL_PROB_FILE)
density_df = pd.read_csv(DENSITY_FILE)
dscp_grp = pd.read_csv(DSCP_FILE, names=['DIS','group'],sep="\t")
grp_adv=pd.read_csv(CNTRY_GRP)

cntry_grp_prob=final_prob.merge(dscp_grp,on='DIS').groupby(['COUNTRY','CRRT_TIME','group'])['st0'].sum().reset_index()
cntry_grp_prob=cntry_grp_prob.pivot_table(index=['COUNTRY','CRRT_TIME'],
                                columns='group',values='st0').reset_index()
cntry_grp_prob=cntry_grp_prob.rename(
columns={'COUNTRY':'country','CRRT_TIME':'year','NE':'ne_exp','NM':'nm_exp','SHM':'shm_exp'})

final_true=density_df[['DIS','st0','COUNTRY','CRRT_TIME']]
cntry_grp_true=final_true.merge(dscp_grp,on='DIS').groupby(['COUNTRY','CRRT_TIME','group'])['st0'].sum().reset_index()
cntry_grp_true=cntry_grp_true.pivot_table(index=['COUNTRY','CRRT_TIME'],
                                columns='group',values='st0').reset_index()
cntry_grp_true.columns=['country','year','ne','nm','shm']
cntry_grp_true=cntry_grp_true.rename(
columns={'COUNTRY':'country','CRRT_TIME':'year','NE':'ne','NM':'nm','SHM':'shm'})

metadata=cntry_grp_true.merge(cntry_grp_prob,on=['country','year'],how='inner')

grp_adv=grp_adv[['COUNTRY','GROUP_ADV','YEAR']]
grp_adv.columns=['country','group','year']

metadata=metadata.merge(grp_adv, on=['country','year'],how='inner')
metadata['nm_diff']=metadata['nm']-metadata['nm_exp']
metadata['ne_diff']=metadata['ne']-metadata['ne_exp']
metadata['shm_diff']=metadata['shm']-metadata['shm_exp']
metadata=metadata[['country','year','group','nm_diff','ne_diff','shm_diff']]
metadata=metadata.melt(id_vars=['country','year','group'],value_vars=['ne_diff','nm_diff','shm_diff'],
value_name='value',var_name='cluster').reset_index()

order=['nm_diff','ne_diff','shm_diff']
g=sns.catplot(x='cluster',y='value',col='group',
data=metadata,kind='box',order=order,color='#4CB1F7')

axes=g.axes.flatten()
titlelist=['Natural','Physical','Societal']
for ind,ax in enumerate(axes):
    ax.axhline(ls="--",linewidth=1,color="grey")
    ax.set_title(titlelist[ind],fontsize=15)
g.set_xticklabels(titlelist,fontsize=12)
g.set_ylabels('Count',fontsize=18)
g.set_xlabels('')
plt.savefig(PLOT_FILE, bbox_inches="tight")
