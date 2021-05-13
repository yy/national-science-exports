"""
This script aggregate gini result in different period into one file

input:
-argv[1]: gini file directory
-argv[2]: s&t index for countries

output:
-argv[3]: aggregated result
"""

import os
import sys
from os.path import join as osjoin

import pandas as pd

GINI_DIR = sys.argv[1]
ST_FILE = sys.argv[2]
AGG_GINI_PATH = sys.argv[3]

st_df = pd.read_csv(ST_FILE, sep="\t", names=["COUNTRY", "ST"])


root, basename = os.path.split(GINI_DIR)
gini_all = pd.DataFrame(columns=["COUNTRY", "GINI", "YEAR"])

for filename in os.listdir(root):
    if basename in filename:
        gini_df = pd.read_csv(osjoin(root, filename))
        year = os.path.splitext(filename)[0].split("_")[2]
        gini_df["YEAR"] = year
        gini_all = pd.concat([gini_all, gini_df], ignore_index=True)

gini_all=gini_all[gini_all.YEAR!='1973-2017']
gini_all.merge(right=st_df, left_on="COUNTRY",
               right_on="COUNTRY").to_csv(AGG_GINI_PATH, index=False)
