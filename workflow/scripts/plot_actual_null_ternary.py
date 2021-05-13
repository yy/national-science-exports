import pandas as pd
import numpy as np
from collections import Counter
import sys
from itertools import product
import ternary

PROXIMITY_NULL_PROB=sys.argv[1]
DSCP_FILE = sys.argv[2]
TERNARY_FILE = sys.argv[3]
YEAR_INTERVAL_FILE=sys.argv[4]
PLOT_FILE = sys.argv[5]



def get_ternaryposition(result_df,dscp_grp):
    grpcount = dscp_grp.groupby('group').size().to_dict()
    ter_df=result_df.merge(dscp_grp,on='DIS')
    ter_df = ter_df.groupby(['COUNTRY','CRRT_TIME','group'])['st0'].sum().reset_index()
    ter_df = ter_df.pivot_table(index=['COUNTRY','CRRT_TIME'],
                                columns='group',values='st0')
    for key, value in grpcount.items():
        ter_df[key]=ter_df[key]/value
    ter_df = ter_df.div(ter_df.sum(axis=1), axis=0).fillna(0).reset_index()
    return ter_df

final_prob= pd.read_csv(PROXIMITY_NULL_PROB)
dscp_grp=pd.read_csv(DSCP_FILE,names=['DIS','group'],sep='\t')

prob_ter=get_ternaryposition(final_prob,dscp_grp)
ter_df=pd.read_csv(TERNARY_FILE)

yearlist=[]
with open(YEAR_INTERVAL_FILE) as f:
    for line in f.readlines():
        yearlist.append(line.strip('\n'))

binlabel=np.arange(1,11,1)/10
start_df=pd.DataFrame()
true_end=pd.DataFrame()
prob_end=pd.DataFrame()
n=0
ter_df = ter_df[~(ter_df[["NE", "NM", "SHM"]] == 0).any(axis=1)]
for i, j in product(binlabel, repeat=2):
    thiscell = ter_df.loc[(ter_df['NE'].between(i-0.1,i))
                          &(ter_df['SHM'].between(j-0.1,j))]
    for index, row in thiscell.iterrows():
        country = row["COUNTRY"]
        year = row["YEAR"]
        if year!='2013-2017':
            year_next_ind = yearlist.index(year)
            year_next = yearlist[year_next_ind + 1]

            data_next = ter_df[
                (ter_df["COUNTRY"]==country) & (ter_df["YEAR"]==year_next)]

            if not data_next.empty:
                start=thiscell.loc[[index]]
                start['label']=n
                start_df=pd.concat([start_df,start])

                prob_next=prob_ter[
                    (prob_ter['COUNTRY']==country)&(prob_ter['CRRT_TIME']==year_next)]
                prob_next['label']=n
                prob_end=pd.concat([prob_end, prob_next])

                data_next['label']=n
                true_end=pd.concat([true_end, data_next])
    n=n+1

scale = 1
figure, tax = ternary.figure(scale=scale)
tax.boundary(linewidth=1.0)
#tax.gridlines(multiple=0.1, color="blue")
tax.gridlines()
figure.set_size_inches(8, 8)
for l in start_df.label.unique():
    start_filter=start_df[start_df.label==l]
    x_start=start_filter['NE'].mean()
    y_start=start_filter['SHM'].mean()
    z_start=start_filter['NM'].mean()

    end_filter=true_end[true_end.label==l]
    x_end=end_filter['NE'].mean()
    y_end=end_filter['SHM'].mean()
    z_end=end_filter['NM'].mean()

    prob_filter=prob_end[prob_end.label==l]
    x_prob=prob_filter['NE'].mean()
    y_prob=prob_filter['SHM'].mean()
    z_prob=prob_filter['NM'].mean()



    x1, y1 = ternary.helpers.project_point([x_start, y_start, z_start])
    x2, y2 = ternary.helpers.project_point([x_end, y_end, z_end])
    xprob,yprob = ternary.helpers.project_point([x_prob, y_prob, z_prob])

    tax.ax.arrow(x1, y1, xprob-x1, yprob-y1, head_width = 0.01, color="#BDC7D6")
    tax.ax.arrow(x1, y1, x2-x1, y2-y1, head_width = 0.01,color='#E8682E')


tax.get_axes().axis('off')
#tax.ticks(axis='lbr', multiple=1, linewidth=1, tick_formats="%.1f")
tax.clear_matplotlib_ticks()
tax.right_corner_label(label="P",fontsize=18)
tax.top_corner_label(label="S",fontsize=18)
tax.left_corner_label(label="N",fontsize=18)
tax.savefig(PLOT_FILE)
