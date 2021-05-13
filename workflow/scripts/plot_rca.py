"""
This script plots a world map where country is color coded by their rca value

input:
-argv[1]: rca file for a specific time period
-argv[2]: country flag table contains country iso-3 code and name variations
          for country in wos, eci, wold bank.
-argv[3]: world map shape file contains geometry information for countries

-argv[4]: path to save the plot
"""

import os
import sys

import geopandas as gp
import matplotlib.pyplot as plt
import nsp.core
import numpy as np
import pandas as pd
from matplotlib import rcParams

RCA_FILE = sys.argv[1]
FLAG_TABLE = sys.argv[2]
WORLD_GEO = sys.argv[3]
PLOT_PATH_DIR = sys.argv[4]

rca_df = pd.read_csv(RCA_FILE)
# rca_df = pd.melt(rca_df, id_vars=["COUNTRY"],var_name='DIS', value_name='VALUE')
flag_table = pd.read_csv(FLAG_TABLE, sep="\t")
world_geo = gp.read_file(WORLD_GEO)[
    ["NAME", "ISO_A3", "geometry", "ADM0_A3", "CONTINENT", "SUBREGION"]
]

rca_flag = rca_df.merge(right=flag_table, left_on="COUNTRY", right_on="WoS")
rca_geo = rca_flag.merge(
    how="inner", right=world_geo, left_on="Code", right_on="ADM0_A3"
)

rca_geo = rca_geo[rca_geo.CONTINENT != "Antarctica"]
world_geo = world_geo[world_geo.CONTINENT != "Antarctica"]
rca_geo = gp.GeoDataFrame(rca_geo)

rca_geo["VALUES"] = rca_geo["VALUES"].apply(
    lambda x: np.log10(x)
)  # transform to logarithm
data_empty = world_geo[
    ~(world_geo["ADM0_A3"].isin(rca_geo["ADM0_A3"]))
]  # countries not covered by wos
vmax = rca_geo["VALUES"].max()

dislist = rca_geo.DIS.unique()
yearlist = rca_geo.YEAR.unique()

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Arial"]

for dis in dislist:
    os.makedirs(os.path.join(PLOT_PATH_DIR, dis))
    for year in yearlist:
        fig, ax = plt.subplots(1, figsize=(10, 6))
        rca_color = rca_geo[
            (rca_geo.DIS == dis) & (rca_geo.YEAR == year) & (rca_geo.VALUES > 0)
        ]
        fig, ax = nsp.core.plot_worldmap(
            ax, fig, world_geo, data_empty, rca_color, "VALUES", "viridis_r", vmax=vmax
        )
        ax.text(
            0.04,
            1,
            dis,
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=16,
        )
        plot_path = os.path.join(PLOT_PATH_DIR, dis, year + "_" + dis + ".pdf")
        plt.savefig(plot_path, format="pdf")
        plt.clf()
    plt.close("all")
# root, basename = os.path.split(PLOT_PATH)
# dis = os.path.splitext(basename)[0].split("_")[1]
# rca_dis = rca_geo[(rca_geo.DIS==dis) & (rca_geo.VALUE>0)]
# ax = nsp.core.plot_worldmap(
# world_geo, data_empty, rca_dis, "VALUE", "viridis_r", vmax=vmax)
# afont = {'fontname':'Arial'}
# ax.text(
#    .04,1,dis,verticalalignment='center',transform=ax.transAxes, fontsize=13, **afont)
# plt.savefig(PLOT_PATH, format="pdf")
