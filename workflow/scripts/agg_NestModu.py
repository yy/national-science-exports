"""
aggeragate the nestedness modularity calculation into one file
"""
import fnmatch
import pandas as pd
import os
from os.path import join as osjoin
import sys

NESTMODU_DIR = sys.argv[1]
AGG_NESTMODU_PATH = sys.argv[2]

collist = ['NodfRes', 'ModuRes', 'Flag','YEAR']
NestModu_all = pd.DataFrame(columns=collist)

for filename in os.listdir(NESTMODU_DIR):
    NestModu_df = pd.read_csv(osjoin(NESTMODU_DIR, filename))
    year = os.path.splitext(filename)[0].split("_")[2]
    NestModu_df["YEAR"] = year
    NestModu_all = pd.concat([NestModu_all, NestModu_df], ignore_index=True)
NestModu_all.to_csv(AGG_NESTMODU_PATH, index=False)