import pandas as pd
import xlrd
import numpy as np
import sys
import ast

INCOME_GROUP = sys.argv[1]
TERNARY_FILE = sys.argv[2]
PERIODS_FILE = sys.argv[3]
TERNARY_INCOME_FILE = sys.argv[4]

incomegroup_df = pd.read_excel(INCOME_GROUP)
incomegroup_df = incomegroup_df.replace(to_replace = "..",value=np.nan)
ternary_df = pd.read_csv(TERNARY_FILE)
with open(PERIODS_FILE) as file:
    PERIODS = file.readlines()
PERIODS = [item.strip("\n") for item in PERIODS][3:]

result_df = pd.DataFrame()
for time in PERIODS:
    start, end = time.split("-")
    cols = list(np.arange(int(start), int(end)+1))
    cols.append("Code")
    subset_df = incomegroup_df[cols]
    mode_df = subset_df.set_index("Code").mode(axis=1, dropna=True).reset_index()[['Code',0]]
    mode_df['YEAR']=time
    result_df = pd.concat([result_df, mode_df])
result_df.columns=['Country Code','IncomeGroup','YEAR']

ternary_df = ternary_df.merge(result_df, left_on=['Country Code','YEAR'], right_on=['Country Code','YEAR'], how="left")
ternary_df.dropna().to_csv(TERNARY_INCOME_FILE, index=False)
