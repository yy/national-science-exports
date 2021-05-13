"""
This script transform string edgelist to id edgelist
input:

-argv[1]:edgelist csv file
-argv[2]:node id mapping file

output (argv[3]): edgelist file with node replaced by integer id

"""
import pandas as pd
import sys
import nsp.core

EDGELIST_CSV = sys.argv[1]
ID2NODE_FILE = sys.argv[2]
EDGELIST_TRANS_CSV = sys.argv[3]

edgelist_df = pd.read_csv(
    EDGELIST_CSV, sep="\t",names=['source','target','weight']
)

node2id = nsp.core.get_mapping(ID2NODE_FILE, k="NODE", v="ID")

edgelist_df.replace(node2id).to_csv(EDGELIST_TRANS_CSV, index=False)
