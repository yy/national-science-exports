""" This script calculate the proximity matrix

input:
- argv[1]: the RCA matrix (rows: countries, cols: disciplines)

output:
- argv[2]: the proximity matrix as edgelist

"""
import sys

import pandas as pd

import nsp.core


RCA_FILE = sys.argv[1]
CSV_FILE_PATH = sys.argv[2]

rca_data = pd.read_csv(RCA_FILE)
rca_data = rca_data.set_index("COUNTRY")
prox = nsp.core.cal_prox(rca_data)
prox = prox.reset_index()
prox = pd.melt(prox, id_vars=["index"])
prox.to_csv(CSV_FILE_PATH, header=False, index=False, sep="\t")
