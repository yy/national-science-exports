"""
This script calculate weighted modularity by partition the
network into advantaged disciplines or disadvantage disciplines
"""
import pandas as pd
import networkx as nx
import sys
import itertools

def cal_modularity(pdict, network):
    degree = dict(nx.degree(network, weight="weight"))
    M = network.size(weight="weight")
    nodes = list(network)
    res = 0
    for i in nodes:
        for j in nodes:
            if (pdict.get(i,0)==pdict.get(j,0)) & (i!=j):
                #res += network_filter.get_edge_data(i,j)['weight']-((degree[i]*degree[j])/(2*M))
                aij = network.get_edge_data(i,j)['weight']
                res =res+ aij-((degree[i]*degree[j])/(2*M))

    return(res/(2*M))

if __name__ == "__main__":
    RCA_FILE = sys.argv[1]
    PROX_MATRIX = sys.argv[2]
    MODU_RES = sys.argv[3]

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

    modu_df = pd.DataFrame(columns=['COUNTRY','PERIOD','MODU'])
    for item in cntryyear:
        country = item[0]
        year = item[1]
        rca_filter = rca_df[(rca_df.COUNTRY==country) & (rca_df.YEAR==year)]
        if not rca_filter.empty:
            partitiondict = dict(zip(rca_filter.DIS,rca_filter.FLAG))
            modu = cal_modularity(partitiondict, network_full)
            modu_df = modu_df.append({'COUNTRY':country,'PERIOD':year, 'MODU':modu},ignore_index=True)

modu_df.to_csv(MODU_RES, index=False)
