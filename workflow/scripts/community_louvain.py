import networkx as nx
import community as community_louvain
import numpy as np
import pandas as pd
import sys

PROX_FILE = sys.argv[1]
COMMUNITY_OUTPUT=sys.argv[2]

prox_df=pd.read_csv(PROX_FILE,sep="\t",names=['source','target','weight'])
graph=nx.from_pandas_edgelist(prox_df,edge_attr='weight')
graph.remove_edges_from(nx.selfloop_edges(graph))

partition=community_louvain.best_partition(graph,weight='weight')

groupid2name_dict={}
labeldiscipline=["Tropical Medicine","Biomedical Engineering","Hematology"]
grouplist=['NM','NE','SHM']
for index, label in enumerate(labeldiscipline):
    groupid2name_dict[partition[label]]=grouplist[index]

partition_df=pd.DataFrame.from_dict(partition,orient='index').reset_index()
partition_df.columns=['dis','group']
partition_df=partition_df.replace({'group':groupid2name_dict})
partition_df.to_csv(COMMUNITY_OUTPUT,index=False)
