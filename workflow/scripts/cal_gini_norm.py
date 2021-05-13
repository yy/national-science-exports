""" This script calculate the gini coeficient and save it to a csv file.
    normed publication count will be used to calculate the gini coeficient

input:
- argv[1]: the publication record file (e.g. `pubcnt_corr.csv`)

output:
- argv[2]: the gini result for the given time period

"""
import sys

import nsp.core
import pandas as pd


def split_full_df(df):
    all_country_df = df[df["COUNTRY"] == "ALL COUNTRIES"]
    pubrec_filtered_df = df[df["COUNTRY"] != "ALL COUNTRIES"]
    return all_country_df, pubrec_filtered_df

if __name__ == "__main__":
    PUBCNT_FILE = sys.argv[1]
    CSV_FILE_PATH = sys.argv[2]
    START_YEAR, END_YEAR = nsp.core.extract_years_from_path(CSV_FILE_PATH)

    pubrec_filtered_df = nsp.core.extract_pubrec_by_timeperiod(
        PUBCNT_FILE, START_YEAR, END_YEAR
    )

    if "full" in PUBCNT_FILE:
        # for the full count data, we use the pre-counted numbers
        all_country_df, pubrec_filtered_df = split_full_df(pubrec_filtered_df)
        numpubs_in_dis = all_country_df.groupby(["SPECIALTY"]).sum()
    else:
        numpubs_in_dis = pubrec_filtered_df.groupby(["SPECIALTY"]).sum()
    
    # When calculating Gini, we treat full count data same as other count data.
    numpubs_in_cntry_dis_df = nsp.core.pubcnt_by_cntry_and_disc(pubrec_filtered_df)

    #convert numpubs_in_dis into series for dividing
    numpubs_in_dis = pd.Series(numpubs_in_dis["PAPER_CNT"], index=numpubs_in_dis.index)
    #normlize each discipline column based on the total number in numpubs_in_dis
    numpubs_in_cntry_dis_df = numpubs_in_cntry_dis_df.div(numpubs_in_dis, axis=1)

    numpubs_in_cntry_dis_df.apply(
        lambda row: nsp.core.gini_coef(row.values), axis=1
    ).to_csv(CSV_FILE_PATH, header=["GINI"], index_label="COUNTRY")
