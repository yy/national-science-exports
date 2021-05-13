""" This script calculates the yearly total publication in each discipline.


argv[1]: the pubcnt csv file for the full
argv[2]: the output file for the yearly total pubcnt in discipline.

"""

import pandas as pd
import sys

PUBCNT_FULL = sys.argv[1]
PUBCNT_DIS_CSV = sys.argv[2]

raw_data = pd.read_csv(PUBCNT_FULL)
raw_data[raw_data["COUNTRY"] == "ALL COUNTRIES"].to_csv(PUBCNT_DIS_CSV, index=False)
# raw_data[raw_data["COUNTRY"] != "ALL COUNTRIES"].to_csv(PUBCNT_FULL, index=False)
