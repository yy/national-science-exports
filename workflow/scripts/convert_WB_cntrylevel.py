import sys
from itertools import islice

import pandas as pd


def cal_avg(df, periods):
    """calculate the average value during period for the data
    i.e. calculate average income between 13-17" """
    for start, end in periods:
        df[f"{start}-{end}"] = df[[str(ind) for ind in range(start, end + 1)]].mean(
            axis=1
        )
    return df


if __name__ == "__main__":
    INCOME_FILE = sys.argv[1]
    INTERVAL_FILE = sys.argv[2]
    CNTRY_YEAR_INCOMEVALUE = sys.argv[3]

    income_df = pd.read_csv(INCOME_FILE, encoding="ISO-8859-1")
    periods = [
        tuple(map(int, x.strip("\n").split("-")))
        for x in islice(open(INTERVAL_FILE), 0, None)
    ]
    income_df = cal_avg(income_df, periods)
    income_df = income_df[
        ["Country Code"] + [f"{start}-{end}" for start, end in periods]
    ]

    income_df.melt(
        id_vars=["Country Code"], var_name="Year", value_name="Income"
    ).rename(columns={"Country Code": "Code"}).to_csv(
        CNTRY_YEAR_INCOMEVALUE, index=False
    )
