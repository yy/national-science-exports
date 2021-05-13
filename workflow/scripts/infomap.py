import infomap
import pandas as pd
import numpy as np
import sys
from infomap import Infomap

PROX_FILE = sys.argv[1]
OUTPUT=sys.argv[2]



prox_file = pd.read_csv(PROX_FILE, sep="\t")

im = infomap.Infomap()

vlist=np.unique(prox_file[['source','target']].values)
vdict={k: ind for ind,k in enumerate(vlist)}
vdict2={ind: k for ind,k in enumerate(vlist)}
net_df=prox_file.replace({'source':vdict,'target':vdict})
links = tuple(map(tuple,net_df.values))
im.add_links(links)

im.run()
resultlist=[]
for node_id,module_id in im.modules:
    resultlist.append([vdict2[node_id],module_id])
group = pd.DataFrame(resultlist,columns=['dis','group'])
group.to_csv(OUTPUT, index=False)
