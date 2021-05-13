"""
This script extract country income group from original file
Match the country code with wos country name
"""
import sys
from itertools import islice

import numpy as np
import pandas as pd

INCOME_GROUP = sys.argv[1]
INTERVAL_FILE = sys.argv[2]
FLAG_TABLE = sys.argv[3]
CNTRY_YEAR_INCOMEGROUP = sys.argv[4]


incomegroup_df = pd.read_excel(INCOME_GROUP, engine="openpyxl").replace(
    to_replace="..", value=np.nan
)
periods = [
    tuple(map(int, x.strip("\n").split("-")))
    for x in islice(open(INTERVAL_FILE), 3, None)
]

result_df = pd.DataFrame()
for (start, end) in periods:
    cols = list(np.arange(start, end + 1)) + ["Code"]
    subset_df = incomegroup_df[cols]
    mode_df = (
        subset_df.set_index("Code").mode(axis=1, dropna=True).reset_index()[["Code", 0]]
    )
    mode_df["YEAR"] = f"{start}-{end}"
    result_df = pd.concat([result_df, mode_df])
result_df.columns = ["Code", "IncomeGroup", "YEAR"]

cntry_flag = pd.read_csv(FLAG_TABLE, sep="\t")
result_df = result_df.merge(cntry_flag[["WoS", "Code"]], on="Code")

result_df.to_csv(CNTRY_YEAR_INCOMEGROUP, index=False)
