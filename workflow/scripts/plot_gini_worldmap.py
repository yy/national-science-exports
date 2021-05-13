"""
This script plots a world map where country is color coded by their gini value

input:
-argv[1]: gini value file
-argv[2]: country flag table contains country iso-3 code and name variations
          for country in wos, eci, wold bank.
-argv[3]: world map shape file contains geometry information for countries

-argv[4]: path to save the plot
"""

import sys

import geopandas as gp
import matplotlib.pyplot as plt
import nsp.core
import pandas as pd

GINI_FILE = sys.argv[1]
FLAG_TABLE = sys.argv[2]
WORLD_GEO = sys.argv[3]
PLOT_PATH = sys.argv[4]

gini_df = pd.read_csv(GINI_FILE)
flag_table = pd.read_csv(FLAG_TABLE, sep="\t")
world_geo = gp.read_file(WORLD_GEO)[
    ["NAME", "ISO_A3", "geometry", "ADM0_A3", "CONTINENT", "SUBREGION"]
]

gini_merge = gini_df.merge(right=flag_table, left_on="COUNTRY", right_on="WoS")
gini_merge = gini_merge.merge(
    how="inner", right=world_geo, left_on="Code", right_on="ADM0_A3"
)

gini_merge = gini_merge[gini_merge.CONTINENT != "Antarctica"]
gini_merge["DIVERSITY"] = 1 - gini_merge["GINI"]
world_geo = world_geo[world_geo.CONTINENT != "Antarctica"]
gini_geo = gp.GeoDataFrame(gini_merge)

data_empty = world_geo[~(world_geo["ADM0_A3"].isin(gini_geo["ADM0_A3"]))]
fig, ax = plt.subplots(1, figsize=(10, 6))
fig, ax = nsp.core.plot_worldmap(
    ax, fig, world_geo, data_empty, gini_geo, "DIVERSITY", cmap="viridis"
)
plt.savefig(PLOT_PATH, format="pdf")
