import pandas as pd
import numpy as np
import sys

GINI_DATA=sys.argv[1]
RCA_DATA=sys.argv[2]
META_DATA=sys.argv[3]

gini_df=pd.read_csv(GINI_DATA)
rca_df=pd.read_csv(RCA_DATA)

gini_df=gini_df[['Code','gini','ECI','period','diversity','growth']]
metadata=rca_df.merge(gini_df,on=['Code','period'],how='left')
metadata['Income_t0_log']=np.log10(metadata['Income_t0'])

metadata.to_csv(META_DATA,index=False)
