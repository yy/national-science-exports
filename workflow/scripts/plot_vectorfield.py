"""
This scripts plot country average tragectory in ternary plot

input:
-argv[1]: ternary file contains country position in each period

output:
-argv[2]: plot path
"""

import pandas as pd
import math
import ternary
import sys
import numpy as np
from itertools import product
from ternary import helpers


TERNARY_FILE = sys.argv[1]
PLOT_PATH = sys.argv[2]

ternary_data = pd.read_csv(TERNARY_FILE)
yearlist = ternary_data.YEAR.unique().tolist()
yearlist.sort()

ternary_data = ternary_data[~(ternary_data[["NE", "NM", "SHM"]] == 0).any(axis=1)]
ternary_data["NE_CELL"] = ternary_data["NE"].apply(lambda x:np.ceil(x*10)/10)
ternary_data["SHM_CELL"] = ternary_data["SHM"].apply(lambda x:np.ceil(x*10)/10)

scale = 1
figure, tax = ternary.figure(scale=scale)
tax.boundary(linewidth=1.0)
tax.gridlines(multiple=0.1, color="blue")
figure.set_size_inches(8, 8)

cell_list = np.arange(0,10,1)/10
for i, j in product(cell_list, repeat=2):
    thiscell = ternary_data.loc[(ternary_data['NE_CELL']==i) & (ternary_data['SHM_CELL']==j)]

    #drop the latest records since no next tragectory to use
    thiscell = thiscell[thiscell["YEAR"] != yearlist[-1]]
    if not thiscell.empty:
        x_pre = thiscell["NE"].mean()
        y_pre = thiscell["SHM"].mean()
        z_pre = 1-x_pre-y_pre

        x_next_list=[]
        y_next_list=[]

        for index, row in thiscell.iterrows():
            country = row["COUNTRY"]
            year_pre = row["YEAR"]
            year_pre_ind = yearlist.index(year_pre)
            year_next = yearlist[year_pre_ind + 1]

            try:
                data_next = ternary_data[(ternary_data["COUNTRY"]==country) & (ternary_data["YEAR"]==year_next)]
                x_next = data_next["NE"].values[0]
                y_next = data_next["SHM"].values[0]
                x_next_list.append(float(x_next))
                y_next_list.append(float(y_next))
            except:
                pass

        x_next = sum(x_next_list)/len(x_next_list)
        y_next = sum(y_next_list)/len(y_next_list)
        z_next = 1 - x_next - y_next

        x1, y1 = ternary.helpers.project_point([x_pre, y_pre, z_pre])
        x2, y2 = ternary.helpers.project_point([x_next, y_next, z_next])
        tax.ax.arrow(x1, y1, x2-x1, y2-y1, head_width = 0.01)

tax.get_axes().axis('off')
tax.ticks(axis='lbr', multiple=0.5, linewidth=1, tick_formats="%.1f")
tax.clear_matplotlib_ticks()
tax.right_corner_label(label="A",fontsize=18)
tax.top_corner_label(label="S",fontsize=18)
tax.left_corner_label(label="R",fontsize=18)
tax.savefig(PLOT_PATH)
