""" This script calculates the group rca for each country at each time period
"""

import sys
import nsp.core
import pandas as pd


PUBCNT_FILE = sys.argv[1]
DSCP_GROUP = sys.argv[2]
INTERVAL_FILE = sys.argv[3]

GROUP_RCA_OUTPUT = sys.argv[4]

pcnt_df = pd.read_csv(PUBCNT_FILE)
dscp_df = pd.read_csv(DSCP_GROUP, sep="\t", names=["DIS","GROUP"])
with open(INTERVAL_FILE) as file:
    interval_list = file.read().splitlines()

group_rca_all = pd.DataFrame()
for period in interval_list:
    start, end= map(int, period.split("-"))
    pubrec_filtered_df = nsp.core.extract_pubrec_by_timeperiod(
        PUBCNT_FILE, start, end)
    pubrec_filtered_df = pubrec_filtered_df.merge(dscp_df, left_on="SPECIALTY", right_on="DIS")
    if "full" in PUBCNT_FILE:
        all_country_df, pubrec_filtered_df = nsp.core.split_full_df(pubrec_filtered_df)
        numpubs_in_group = all_country_df.groupby(['GROUP']).sum()
    else:
        numpubs_in_group = pubrec_filtered_df.groupby(['GROUP']).sum()
    numpubs_total = numpubs_in_group['PAPER_CNT'].sum()
    numpubs_in_cntry = pubrec_filtered_df.groupby(['COUNTRY']).sum()
    numpubs_in_cntry_group_df = nsp.core.pubcnt_by_cntry_and_group(pubrec_filtered_df)

    rca_df = nsp.core.cal_rca(
    numpubs_in_cntry, numpubs_in_group, numpubs_total, numpubs_in_cntry_group_df
    )
    rca_df["GROUP_ADV"] = rca_df.idxmax(axis=1)
    rca_df["YEAR"] = period
    group_rca_all = pd.concat([rca_df, group_rca_all])

    group_rca_all.to_csv(GROUP_RCA_OUTPUT)
