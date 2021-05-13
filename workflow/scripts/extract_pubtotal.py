""" This script calculates the yearly total publication.

argv[1]: the discipline-based aggregated count csv.
argv[2]: the output file for the yearly total pubcnt.

"""

import pandas as pd
import sys

PUBCNT_DIS_CSV = sys.argv[1]
PUBCNT_GLOBAL_CSV = sys.argv[2]

pd.read_csv(PUBCNT_DIS_CSV).to_csv(PUBCNT_GLOBAL_CSV, index=False)
