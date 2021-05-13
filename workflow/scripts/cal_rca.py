""" This script cleans the raw pubrec_df and saves into a csv file.

input:
- argv[1]: the publication record file (e.g. `pubcnt_corr.csv`)
- argv[2]: the start year of the desired calculation
- argv[3]: the end year of the desired calculation

output:
- argv[4]: the rca result for each time period

"""
import os
import sys

import nsp.core


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

    numpubs_total = numpubs_in_dis["PAPER_CNT"].sum()
    numpubs_in_cntry = pubrec_filtered_df.groupby(["COUNTRY"]).sum()
    numpubs_in_cntry_dis_df = nsp.core.pubcnt_by_cntry_and_disc(pubrec_filtered_df)

    nsp.core.cal_rca(
        numpubs_in_cntry, numpubs_in_dis, numpubs_total, numpubs_in_cntry_dis_df
    ).to_csv(os.path.join(CSV_FILE_PATH))
