"""
This script sample publications to test the validity of gini on country level

input:
-argv[1]: publication record
-argv[2]: time period

output:
-argv[3]: bootstrap result
"""

import pandas as pd
from collections import Counter
import numpy as np
import sys
import nsp.core
import argparse
import ast

# parse = argparse.ArgumentParser()
# parse.add_argument("--inputfile", help="input file path")
# parse.add_argument("--periodlist", type=list, help="list contains time periods")
# parse.add_argument("--outputfile", help="output file path")
# arg = parse.parse_args()

PCNT_FILE = sys.argv[1]
#PERIODS = sys.argv[2]
OUTPUT_FILE = sys.argv[2]

N=100
smple_pf_start, smple_pf_end = 1973,1977
smple_pf_df = nsp.core.get_sample_profile(PCNT_FILE, smple_pf_start, smple_pf_end)
START_YRS = list(range(1973, 2018, 5))
END_YRS = list(range(1977, 2018, 5))
PERIODS = ['{}-{}'.format(sy, ey) for sy, ey in zip(START_YRS, END_YRS)]

avggini_all_df = pd.DataFrame()
#PERIODS = PERIODS.strip('[]').split(',')
for period in PERIODS:
    print(period)
    start, end = map(int, period.split("-"))
    pcnt_filtered_df = nsp.core.extract_pubrec_by_timeperiod(PCNT_FILE, start, end)

    if "full" in PCNT_FILE:
        pcnt_all_df, pcnt_filtered_df = nsp.core.split_full_df(pcnt_filtered_df)
    numpubs_in_cntry_df = pcnt_filtered_df.groupby(["COUNTRY"]).sum()
    numpubs_in_cntry_df["PAPER_CNT"] = numpubs_in_cntry_df["PAPER_CNT"].apply(lambda x: np.int(np.ceil(x)))
    dscplist = pcnt_filtered_df.SPECIALTY.unique()
    avggini_temp = nsp.core.cal_save_btstrping(smple_pf_df, numpubs_in_cntry_df, dscplist, nsp.core.gini_coef, "GINI", N)
    avggini_temp['year'] = period
    avggini_all_df = pd.concat([avggini_all_df, avggini_temp], ignore_index=True)

avggini_all_df.to_csv(OUTPUT_FILE, index=False)




    # calculate gini by the normalized publication number
    # if "full" in PCNT_FILE:
    #     pcnt_all_df, pcnt_filtered_df = nsp.core.split_full_df(pcnt_filtered_df)
    #     numpubs_in_dis = pcnt_all_df.groupby("SPECIALTY").sum()
    # else:
    #     numpubs_in_dis = pcnt_filtered_df.groupby("SPECIALTY").sum()

    # numpubs_in_dis = pd.Series(numpubs_in_dis["PAPER_CNT"], index=numpubs_in_dis.index)
    # numpubs_in_cntry_df = pcnt_filtered_df.groupby(["COUNTRY"]).sum()
    # numpubs_in_cntry_df["PAPER_CNT"] = numpubs_in_cntry_df["PAPER_CNT"].apply(lambda x: np.int(np.ceil(x)))

    # nsp.core.cal_save_btstrping(smple_pf_df, numpubs_in_cntry_df, numpubs_in_dis, nsp.core.gini_coef, "GINI", N, OUTPUT_FILE)
