"""This script calculates the modularity of individual country knowledge space
over time.
Network group is defined by RCA value(whether RCA large than 1 or not)
"""
import pandas as pd
import community
import sys
import networkx as nx

RCA_FILE = sys.argv[1]
PROX_NET_FILE = sys.argv[2]
COUNTRY_ST = sys.argv[3]
MODU_FILE = sys.argv[4]

rca_df = pd.read_csv(RCA_FILE)
network_full = nx.read_weighted_edgelist(PROX_NET_FILE)
cntry_st = pd.read_csv(COUNTRY_ST, sep="\t", names=['COUNTRY','ST'])

rca_df = rca_df[rca_df.DIS!="Unknown"]
network_full.remove_node("Unknown")
network_full.remove_edges_from(nx.selfloop_edges(network_full))

cntrylist = rca_df.COUNTRY.unique()
yearlist = rca_df.YEAR.unique()
cntryyear = list(itertools.product(cntrylist, yearlist))
rca_df['FLAG'] = rca_df['VALUES'].apply(lambda x: 1 if x>1 else 0)

modu_df = pd.DataFrame(columns=['COUNTRY','PERIOD','MODU'])
for item in cntryyear:
    country = item[0]
    year = item[1]
    rca_filter = rca_df[(rca_df.COUNTRY==country) & (rca_df.YEAR==year)]
    if not rca_filter.empty:
        partitiondict = dict(zip(rca_filter.DIS,rca_filter.FLAG))
        modu = community.modularity(partitiondict, netfull, weight='weight')
        modu_df = modu_df.append({'COUNTRY':country,'PERIOD':year, 'MODU':modu},ignore_index=True)

modu_df.merge(cntry_st, on="COUNTRY").to_csv(MODU_FILE, index=False)
