"""
This script aggerate income data with ternary data and filter out the rows with no income data.
Each row records a ternary point for a country in a specific time.

input:
-argv[1]: the ternary data contains countries' ternary position in a specific time
-argv[2]: GDP data

output:
-argv[3]: aggregated ternary data
"""

import pandas as pd
import numpy as np
import sys


TERNARY_FILE_PATH = sys.argv[1]
GDP_FILE_PATH = sys.argv[2]
TER_META_PATH = sys.argv[3]

def year_split(period):
    start, end = map(int, period.split("-"))
    return start, end

def avg_income(periodlist, income_df):
    for period in periodlist:
        start, end = year_split(period)
        incomeavg = income_df[[str(ind) for ind in np.arange(start,end+1)]].mean(axis=1)
        income_df[period] = incomeavg
    return income_df

ternary_raw = pd.read_csv(TERNARY_FILE_PATH)
income_df = pd.read_csv(GDP_FILE_PATH)

periodlist = ternary_raw.YEAR.unique()
income_df = avg_income(periodlist, income_df)

cols = np.append(["Country Code"], periodlist)
income_df = income_df[cols]
income_df = income_df.melt(id_vars="Country Code", var_name="YEAR", value_name="INCOME")
income_df['INCOME'] = np.log10(income_df['INCOME'])

ter_meta = ternary_raw.merge(right=income_df, how="left", left_on=["Country Code", "YEAR"], right_on=["Country Code", "YEAR"])
ter_meta.dropna().to_csv(TER_META_PATH, index=False)
