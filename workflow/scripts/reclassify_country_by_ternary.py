"""
reclassify the country by their positions in ternary plot
during the earliest period
"""
import pandas as pd
import sys

TERNARY_DATA_PATH = sys.argv[1]
OUTPUT_PATH = sys.argv[2]

ternary_df = pd.read_csv(TERNARY_DATA_PATH)

ternary_early = ternary_df[ternary_df.YEAR=='1973-1977']
ternary_early['maxgroup'] = ternary_early[['NM','NE','SHM']].idxmax(axis=1)
for i, row in ternary_early.iterrows():
    maxgroup = row['maxgroup']
    maxgroup_value = row[maxgroup]
    ternary_group='diverse'
    if maxgroup_value >0.5:
        ternary_group = maxgroup
    ternary_early.at[i,'ternary_group'] = ternary_group

cntry_grp = ternary_early[['COUNTRY','ternary_group']]
ternary_df = ternary_df.merge(cntry_grp, on='COUNTRY')
ternary_df.to_csv(OUTPUT_PATH, index=False)
