""" This script generate clusters through modularity optimization

input:
- argv[1]: the network file with header

output:
- argv[2]: the community result, first column is node,
second column is the community.

"""
import pandas as pd
import networkx as nx
import numpy as np
import sys
import operator

def read_network(NETWORK_FILE):
    network_df = pd.read_csv(
        NETWORK_FILE, sep="\t", header=0)
    graph = nx.from_pandas_dataframe(
        network_df, source="source", target="target")
    return graph

def cal_modularity_change(node, group, community_dict, graph, m):
    node_in = community_dict[node]
    k_i_in = len(nx.edge_boundary(graph,[node],node_in))
    k_i = graph.degree(node)
    total_weight_in = sum(graph.degree(i) for i in node_in)
    modu_change = (k_i_in/m) + (total_weight_in * k_i)/(2 * m * m)
    return modu_change

if __name__ == "__main__":
    NETWORK_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]

    graph = read_network(NETWORK_FILE)

    prelist = [["General & Internal Medicine", "Botany", "Virology", 
            "Agricult & Food Science", "Environmental Science","Geology"],
            ["Biomedical Engineering", "Physical Chemistry", 
                "General Chemistry", "Materials Science", "Applied Physics"],
            ["Cancer", "Surgery", "Cardiovascular System", 
            "Neurology & Neurosurgery", "Otorhinolaryngology", "Endocrinology"]
            ]
    grouplist=["medical", "eng", "soc"]
    community_dict = dict(map(lambda x,y:[x,y],grouplist, prelist))
    m = graph.number_of_edges()

    #nodes not in the predefined list
    node_res = set(graph.nodes()) - set([item for sublist in prelist for item in sublist])
    for node in node_res:
        modu_result_dict = {}
        for group in grouplist:
            modu_change = cal_modularity_change(node, group, community_dict, graph, m)
            modu_result_dict[group] = modu_change
        group_max = max(modu_result_dict.items, key=operator.itemgetter(1))[0]
        community_dict[group_max].append(node)
    
    fout = open(OUTPUT_FILE, "w")
    for key, value in community_dict.items():
        for index in range(0, len(value)):
            fout.write("%s\t%s\n" %(value[index],key))
    fout.flush()
    fout.close()


    