import numpy as np
import pandas as pd
import leidenalg
import igraph as ig
import sys

PROX_FILE = sys.argv[1]
LEIDEN_WHOLE=sys.argv[2]
LEIDEN_RESULT=sys.argv[3]

prox_df=pd.read_csv(PROX_FILE,sep="\t",names=['source','target','weight'])
whole_df=pd.read_csv(LEIDEN_WHOLE,sep="\t",names=['dis','whole'])

prox_df=prox_df[prox_df.source>prox_df.target]
tuples=[tuple(x) for x in prox_df.values]
graph=ig.Graph.TupleList(tuples,directed=False,edge_attrs=['weight'])
print(graph.ecount())

group=leidenalg.find_partition(graph,leidenalg.ModularityVertexPartition,weights='weight',
n_iterations=100)

resultlist=[]
for v in graph.vs:
    resultlist.append([v['name'],group.membership[v.index]])
rdf=pd.DataFrame(resultlist,columns=['dis','group'])
rdf['group_index']=rdf['group']

groupmarker=["Tropical Medicine","Applied Mathematics","Philosophy"]
labels=['NM','NE','SHM']
for index,marker in enumerate(groupmarker):
    g=rdf[rdf.dis==marker]['group'].values[0]
    rdf=rdf.replace({'group':{g:labels[index]}})

rdf=rdf.merge(whole_df,on="dis")
rdf.to_csv(LEIDEN_RESULT,sep=",",index=False)
