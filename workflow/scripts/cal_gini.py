""" This script calculate the gini coeficient and save it to a csv file.

input:
- argv[1]: the publication record file (e.g. `pubcnt_corr.csv`)

output:
- argv[2]: the gini result for the given time period

"""
import sys

import nsp.core


if __name__ == "__main__":
    PUBCNT_FILE = sys.argv[1]
    CSV_FILE_PATH = sys.argv[2]
    START_YEAR, END_YEAR = nsp.core.extract_years_from_path(CSV_FILE_PATH)

    pubrec_filtered_df = nsp.core.extract_pubrec_by_timeperiod(
        PUBCNT_FILE, START_YEAR, END_YEAR
    )

    # if type='full', there are "ALL COUNTRIES". drop them.
    pubrec_filtered_df = nsp.core.drop_all_countries_entry(pubrec_filtered_df)

    # When calculating Gini, we treat full count data same as other count data.
    numpubs_in_cntry_dis_df = nsp.core.pubcnt_by_cntry_and_disc(pubrec_filtered_df)
    numpubs_in_cntry_dis_df.apply(
        lambda row: nsp.core.gini_coef(row.values), axis=1
    ).to_csv(CSV_FILE_PATH, header=["GINI"], index_label="COUNTRY")
