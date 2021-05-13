"""
This script prepares data for ternary plot. For each country in every period, count the ratio of advantage in each cluster 

input:
-argv[1]: aggregated rca file contains rca value for each country at all the 9 periods
-argv[2]: discipline classification data records in group member of each discipline

output:
-argv[3]: metadata records group ratio for every country
"""

import pandas as pd
import os
from os.path import join as osjoin
import sys


RCA_AGG = sys.argv[1]
DIS_GROUP = sys.argv[2]
FLAG_TABLE = sys.argv[3]
TERNARY_DATA = sys.argv[4]

rca_agg_df = pd.read_csv(RCA_AGG)
dis_group_df = pd.read_csv(
    DIS_GROUP, sep="\t", header=None, names=["DIS", "GROUP"])
flag_table = pd.read_csv(FLAG_TABLE, sep="\t")[["WoS", "Code"]]
flag_table.columns = ["COUNTRY", "Country Code"]
metadata = rca_agg_df.merge(right=dis_group_df, left_on="DIS", right_on="DIS")
#count the number of accurance of each group 
metadata = metadata[metadata.VALUES > 1][["COUNTRY", "YEAR", "GROUP", "ST"]].groupby(
    ['COUNTRY', "YEAR", "ST", "GROUP"]).size().reset_index().rename(columns={0: "COUNT"})
metadata = metadata.pivot_table(index=["COUNTRY","YEAR","ST"], columns="GROUP",values="COUNT" ).reset_index()
metadata = metadata.merge(flag_table, how="left", left_on="COUNTRY", right_on="COUNTRY")

# normalized by the number of disciplines in each group
ne_num = dis_group_df.groupby("GROUP").count().at["NE","DIS"]
nm_num = dis_group_df.groupby("GROUP").count().at["NM","DIS"]
shm_num = dis_group_df.groupby("GROUP").count().at["SHM","DIS"]
metadata = metadata.fillna(0)
group_norm = [nm_num, ne_num, shm_num]
metadata = metadata[['COUNTRY','Country Code','YEAR','ST','NM','NE','SHM']]
cols=["NM","NE","SHM"]
metadata[cols] = metadata[cols].div(group_norm, axis=1)

#normalize to 1
metadata[cols] = metadata[cols].div(metadata[cols].sum(axis=1), axis=0)

metadata.to_csv(TERNARY_DATA, index=False)
