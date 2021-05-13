"""
This script detect communities with stochastic block
model. Due to the randomness in sbm, a voting process
is implemented. Node will be devide to the community which
it has the highest frequence.

input:
-argv[1]: edgelist file
-argv[2]: node and id mapping file

output:
-argv[3]: node and the community the node belongs to
"""

import pandas as pd
import numpy as np
from graph_tool.all import *
import sys
from collections import defaultdict
import nsp.core

NETWORK_FILE = sys.argv[1]
#NODE2ID_FILE = sys.argv[2]
NODEGROUP_FILE = sys.argv[2]
GROUPDETAIL_FILE=sys.argv[3]

network_file=pd.read_csv(NETWORK_FILE,sep="\t")

vlist = np.unique(network_file[['source','target']].values)
elist=network_file[['source','target']].values
wlist=network_file['weight'].values
vmap={}
graph=Graph(directed=False)
vprop=graph.new_vertex_property("string")
eprop=graph.new_edge_property('double')
for vt in vlist:
    v=graph.add_vertex()
    vmap[vt]=v
    vprop[v]=vt
for index,e in enumerate(elist):
    edge = graph.add_edge(vmap[e[0]],vmap[e[1]])
    eprop[edge]=wlist[index]


remove_self_loops(graph)
remove_parallel_edges(graph)

#node2id = nsp.core.get_mapping(NODE2ID_FILE, k="NODE", v="ID")
#id2node = nsp.core.get_mapping(NODE2ID_FILE)

# create 3 markers for three communities
marker_dict = {}
id_TM = vmap["Tropical Medicine"]
marker_dict[id_TM] = "NM"
id_BE = vmap["Biomedical Engineering"]
marker_dict[id_BE] = "NE"
id_HEM = vmap["Hematology"]
marker_dict[id_HEM] = "SHM"

voting_num = 50
voting_dict = defaultdict(list)
resultlist=[]
for iter_time in np.arange(0, voting_num):
    print(iter_time)
    state = minimize_blockmodel_dl(graph, B_min=3, B_max=3,deg_corr=False)
    group = state.get_blocks()

    group_ind2name_dict = {}
    for key, value in marker_dict.items():
        group_ind2name_dict[group[key]] = value

    for node in graph.vertices():
        node_group_name = group_ind2name_dict[group[node]]
        resultlist.append([vprop[node],node_group_name])

result_df = pd.DataFrame(resultlist, columns=['dis','group']).groupby(["dis",'group']).size().reset_index()
result_df.columns=['dis','group','count']
result_df = result_df.pivot(index="dis", columns='group', values='count')
result_df = result_df.fillna(0)
result_df['group']=result_df.idxmax(axis=1)
result_df = result_df.reset_index()
result_df[['dis','group']].to_csv(NODEGROUP_FILE, header=False, sep="\t", index=False)

result_df.to_csv(GROUPDETAIL_FILE, index=False)
