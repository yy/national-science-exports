import pandas as pd
import numpy as np
import networkx as nx
from NODF import NestednessCalculator
import copy
import random
import sys
import nsp.core


DSCP_FILE=sys.argv[1]
CNTRY_GRP= sys.argv[2]
RCA_ALL = sys.argv[3]
NULLRESULT = sys.argv[4]

def bipart_edge_swap(G, max_tries=100, n_swap=2):
    # swap edges of the bipartite network.
    # max_tries: the maximum time try to swap the edges
    # n_swap: the number of time go over the process

        for _ in np.arange(n_swap):
            edgeold=copy.deepcopy(G.edges())
            for src_i, tar_i in edgeold:
                if G.has_edge(src_i, tar_i):
                    numtried=0
                    #print(src_i+\" \"+tar_i)
                    while numtried<max_tries:
                        src_v, tar_v  = random.sample(G.edges(),k=1)[0]
                        if (tar_v not in G[src_i]) and (tar_i not in G[src_v]):
                            #print(src_i+\" \"+tar_i)\n",
                            #print(src_v+\" \"+tar_v)\n",
                            G.add_edge(src_i, tar_v)
                            G.add_edge(src_v, tar_i)
                            G.remove_edge(src_i, tar_i)
                            G.remove_edge(src_v, tar_v)
                            break
                        else:
                            numtried+=1
        return G


def from_edgelist_pandas(graph):
    dflist=[]
    for a, b in graph.edges():
        dflist.append([a,b,1])
    df=pd.DataFrame(dflist, columns=['COUNTRY','DIS','VALUE'])
    df=df.pivot(index='COUNTRY',columns='DIS',values='VALUE')
    df=df.fillna(0)
    return df


dscp_grp = pd.read_csv(DSCP_FILE, sep="\t", names=['col','group'])
cntry_grp = pd.read_csv(CNTRY_GRP)
rca_all = pd.read_csv(RCA_ALL)
periods = rca_all.YEAR.unique()

resultlist = []
for year in periods:
    cntry_grp_year=cntry_grp[cntry_grp.YEAR==year][['COUNTRY','GROUP_ADV']]
    cntry_grp_year.columns=['index','group']
    rca_subset=rca_all[rca_all.YEAR==year]
    rcasub_df = rca_subset.pivot(index='COUNTRY',columns='DIS',values='VALUES')
    rcasub_df[rcasub_df>1]=1
    rcasub_df[rcasub_df<1]=0
    nodf = NestednessCalculator(rcasub_df.values).nodf(rcasub_df.values)
    modu = nsp.core.bipart_modularity(rcasub_df, cntry_grp_year, dscp_grp)
    nodfnull=[]
    modunull=[]
    rca_network = rca_subset[rca_subset.VALUES>1][['COUNTRY','DIS']]
    for a in np.arange(50):

        g = nx.from_pandas_edgelist(rca_network, source='COUNTRY', target='DIS',
                                    create_using=nx.DiGraph)
        gnull=bipart_edge_swap(g)
        null_df=from_edgelist_pandas(gnull)
        nodf_null = NestednessCalculator(null_df.values).nodf(null_df.values)
        modu_null = nsp.core.bipart_modularity(null_df, cntry_grp_year, dscp_grp)
        nodfnull.append(nodf_null)
        modunull.append(modu_null)
    znodf=(nodf-np.mean(nodfnull))/np.std(nodfnull)
    zmodu=(modu-np.mean(modunull))/np.std(modunull)
    resultlist.append([year,'nest',nodf,nodfnull,znodf])
    resultlist.append([year,'modu',modu,modunull,zmodu])
pd.DataFrame(resultlist,
columns=['year','prop','actual','null','zscore']).to_csv(NULLRESULT,index=False)
