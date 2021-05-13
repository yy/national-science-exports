"""
This script calculates the cluster coefficient of network which is formed by
advantage disciplines
"""

import pandas as pd
import networkx as nx
import sys
import itertools


RCA_FILE = sys.argv[1]
PROX_MATRIX = sys.argv[2]
CC_RES = sys.argv[3]

rca_df = pd.read_csv(RCA_FILE)
network_full = nx.read_weighted_edgelist(PROX_MATRIX, delimiter="\t")
network_full.remove_edges_from(nx.selfloop_edges(network_full))
rca_df= rca_df[rca_df.DIS!="Unknown"]
network_full.remove_node("Unknown")

cntrylist = rca_df.COUNTRY.unique()
yearlist = rca_df.YEAR.unique()
cntryyear = list(itertools.product(cntrylist, yearlist))

# partition the network by their rca value
rca_df['FLAG'] = rca_df['VALUES'].apply(lambda x: 1 if x>1 else 0)

cc_df = pd.DataFrame(columns=['COUNTRY','PERIOD','MODU'])
for item in cntryyear:
    country = item[0]
    year = item[1]
    rca_filter = rca_df[(rca_df.COUNTRY==country) & (rca_df.YEAR==year)]
    if not rca_filter.empty:
        advlist = rca_filter[rca_filter.FLAG==1].DIS.tolist()
        subnetwork = network_full.subgraph(advlist)
        cc = nx.average_clustering(subnetwork,weight='weight')
        cc_df = cc_df.append({'COUNTRY':country,'PERIOD':year, 'MODU':cc},ignore_index=True)

cc_df.to_csv(CC_RES, index=False)
