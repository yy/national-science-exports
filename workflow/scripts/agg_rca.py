"""
This script aggregate rca result in different period into one file

input:
-argv[1]: rca file directory
-argv[2]: s&t index for countries
-argv[3]: discipline classification file contains discipline and their group name

output:
-argv[4]: aggregated result
"""

import os
import sys
from os.path import join as osjoin

import pandas as pd

RCA_DIR = sys.argv[1]
ST_FILE = sys.argv[2]
# DIS_GROUP = sys.argv[3]
AGG_GINI_PATH = sys.argv[3]

st_df = pd.read_csv(ST_FILE, sep="\t", names=["COUNTRY", "ST"])
# dis_group = pd.read_csv(DIS_GROUP, sep="\t", header=None,  names=["DIS", "GROUP"])


root, basename = os.path.split(RCA_DIR)
rca_all_list = []
print(root)
print(basename)
for filename in os.listdir(root):
    if basename in filename:
        rca_df = pd.read_csv(osjoin(root, filename))
        rca_df = pd.melt(
            rca_df, id_vars=["COUNTRY"], var_name="DIS", value_name="VALUES"
        )
        year = os.path.splitext(filename)[0].split("_")[2]
        rca_df["YEAR"] = year
        rca_all_list.append(rca_df)

rca_all_df = pd.concat(rca_all_list, ignore_index=True)
# rca_all_df = rca_all_df.merge(right=dis_group, right_on="DIS", left_on="DIS")
rca_all_df = rca_all_df[rca_all_df.YEAR != "1973-2017"]

rca_all_df.merge(right=st_df, left_on="COUNTRY", right_on="COUNTRY").to_csv(
    AGG_GINI_PATH, index=False
)

