import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import bootstrap_disadv as bdv
from matplotlib.lines import Line2D
import matplotlib as mpl
import statsmodels.api as sm

DENSITY_FILE = sys.argv[1]
ST_TABLE = sys.argv[2]
DENSITY_PLOT_PATH = sys.argv[3]

density_df = pd.read_csv(DENSITY_FILE)
st_table = pd.read_csv(ST_TABLE,sep="\t",names=['COUNTRY','ST'])

density_df = density_df.merge(st_table, on="COUNTRY", how="left")
bins = np.arange(0,1.05,0.05)
labels=labels = np.arange(0.05,1.05,0.05)
density_df['binned'] = pd.cut(density_df['Density'], bins, labels = labels,include_lowest=True)
density_df = density_df.replace({'ST':{'Others':'Lagging'}})
density_df = density_df[density_df.DIS!="Unknown"]

cntry_group=['Lagging','Developing','Proficient','Advanced']
mpl.rcParams['axes.linewidth'] = 0.6
fig, ax = plt.subplots()
slopelist=[]
cilist=[]
colormap=['#1B65A6','#9BDAF2','#E8C434','#B980F2']
for index in range(4):
    density_selected = density_df[density_df.ST==cntry_group[index]]
    data_subset = density_selected.loc[:,['st0','st1','binned']].values
    x,y=bdv.bootstrap(data_subset,bdv.theta1_coef)
    sns.regplot(x,y,ax=ax,scatter_kws={'s':1},color=colormap[index],
    line_kws={'linewidth':0.5})

    x2=sm.add_constant(x)
    mod=sm.OLS(y,x2)
    res=mod.fit()
    slopelist.append(np.around(res.params[1],2))
    cilist.append(np.around(res.conf_int()[1],2))
labels = []
for ind in np.arange(4):
    slope=slopelist[ind]
    low=cilist[ind][0]
    high=cilist[ind][1]
    s='Slope:'+str(slope)+" (95% CI:"+str(low)+"--"+str(high)+")"
    labels.append(s)

custom_lines=[Line2D([0],[0],color=colormap[0]),
              Line2D([0],[0],color=colormap[1]),
              Line2D([0],[0],color=colormap[2]),
              Line2D([0],[0],color=colormap[3])]
plt.legend(custom_lines, labels=labels,frameon=False,fontsize=12)
plt.xlim(0)
plt.ylim(0)
ax.text(0.05,0.78,'L&O',fontsize=11)
ax.text(0.05,0.6,'D',fontsize=11)
ax.text(0.05,0.5,'P',fontsize=11)
ax.text(0.17,0.24,'A',fontsize=11)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Density",fontsize=16)
plt.ylabel("Deactivation Probability", fontsize=16)
plt.savefig(DENSITY_PLOT_PATH, format="pdf",bbox_inches="tight")


'''
    thetalist.append(theta_hat_sampling)
    constant = np.mean(constant_sample)
    x,bar,error = bdv.get_bar_values(sample_df)
    #ax[index].errorbar(x, y, yerr=error,ecolor='blue',fmt='--o')

    theta = np.mean(theta_hat_sampling)
    y=constant+theta*x

    theta_up=np.percentile(theta_hat_sampling, 97.5)
    y_up=constant+theta_up*x

    theta_low=np.percentile(theta_hat_sampling, 2.5)
    y_low=constant+theta_low*x

    ax[index].plot(x,y,color="#5C72F2")
    ax[index].fill_between(x,y,y_up, facecolor="#D9D9D9")
    ax[index].fill_between(x,y_low,y, facecolor="#D9D9D9")


    ax[index].annotate(s=r'$y={%.2f}{%.2f}x$'% (constant,theta), xy=(0.3,0.8),
                       xycoords="axes fraction", fontsize=17)
    s=r'$[{%.2f},{%.2f}]$'%(theta_low,theta_up)
    ax[index].annotate(s=s, xy=(0.32,0.7),xycoords="axes fraction", fontsize=12)
    ax[index].set_xticks([0.0,0.2,0.4,0.6,0.8])
    ax[index].set_yticks(np.arange(10)/10)
    ax[index].tick_params(axis='both',labelsize=14)
    ax[index].set_xlabel(cntry_group[index], fontsize=18)
ax[0].set_ylabel("Deactivation Probability", fontsize=16)
plt.savefig(DENSITY_PLOT_PATH, format="pdf",bbox_inches="tight")

fig, ax = plt.subplots(1,4,figsize=(20,5))
for index in range(4):
    theta_hat_sampling = thetalist[index]
    sns.kdeplot(theta_hat_sampling, ax=ax[index])
    ax[index].set_xlabel(xlabel=cntry_group[index], fontsize=18)
    ax[index].set_yticks(np.arange(0,9,1))
    ax[index].set_xticks([-1.6,-1.4,-1.2,-1,-0.8,-0.6])
    ax[index].tick_params(axis='both',labelsize=14)

ax[0].set_ylabel("Density", fontsize=18)
plt.savefig(THETA_PLOT_PATH, format="pdf",bbox_inches="tight")
'''
