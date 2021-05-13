"""create a mapping relationship between discipline and a interger id
input:
argv[1]: file constains all the discipline, here pubcnt_full.csv is used

output:
argv[2]: mapping result output is num:node
argv[3]: mapping result output is node:num

"""

import pandas as pd
import sys
DIS_FILE = sys.argv[1]
ID2NODE_FILE = sys.argv[2]

dis_df = pd.read_csv(DIS_FILE)
dis_list = dis_df.SPECIALTY.unique()

with open(ID2NODE_FILE, "w") as fid2node:
    fid2node.write("{}\t{}\n".format("ID", "NODE"))
    for id, node in enumerate(dis_list):
        fid2node.write("{}\t{}\n".format(id, node))
        