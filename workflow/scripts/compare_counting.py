import pandas as pd
import sys

FULL_FILE=sys.argv[1]
FRAC_FILE=sys.argv[2]
CORR_FILE=sys.argv[3]
OUTPUT=sys.argv[4]

full=pd.read_csv(FULL_FILE,sep='\t',names=['dis','Full'])
frac=pd.read_csv(FRAC_FILE,sep='\t',names=['dis','Fractional'])
corr=pd.read_csv(CORR_FILE,sep='\t',names=['dis','Corresponding'])

meta=full.merge(frac,on='dis')
meta=meta.merge(corr,on='dis')
disdict={'SHM':'S','NE':'P','NM':'N'}
meta=meta.replace({'SHM':disdict,'NE':disdict,'NM':disdict})
meta[(meta['Full']!=meta['Fractional'])|(meta['Full']!=meta['Corresponding'])].to_csv(OUTPUT)
