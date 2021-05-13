import pandas as pd
import numpy as np
import xlrd
import sys

GEO_PATH = sys.argv[1]
TERNARY_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]

geo_df = pd.read_excel(GEO_PATH)
ternary_df = pd.read_csv(TERNARY_FILE)
meta_df = ternary_df.merge(geo_df[["Code",'Region']], left_on="Country Code",right_on="Code", how="left")
meta_df.dropna().to_csv(OUTPUT_FILE, index=False)
