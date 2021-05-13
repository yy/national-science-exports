"""
This script count the expected developing density of a discipline and actual
transition probability
"""

import pandas as pd
import numpy as np
import sys


def assign_sig(rca_df):
    """assign a flag to discipline indicates whether it is advantaged """
    rca_df["FLAG_ADV"] = rca_df["RCA"].apply(lambda x: 1 if x >= 1 else 0)
    return rca_df


def extract_time_signal(cntry_time_df, dscplist, colname):
    time_flag_df = (
        cntry_time_df[["DIS", "FLAG_ADV"]]
        .set_index("DIS")
        .reindex(dscplist)
        .rename(columns={"FLAG_ADV": colname})
    )
    time_flag_df = time_flag_df.fillna(0)
    return time_flag_df

def cal_exp(cntry_df, st0_df, st1_df, prx_mat, dscplist):
    """calculate the expected transition probability by calculating the average
    density around the targeted discipline
    returned dataframe contains three columns:
    index: discipline
    density: average density derived from the rest of disciplines
    st0: flag indicates whether the discipline is advantaged in the current step
    st1: flag indicates whether the discipline is advantaged in the next step
    """


    """derived density by the dot product of the density row and st0 vector which indicates
    whether the discipline is advantaged or not.
    Normalized the density of each discipline by the total density
    """
    neighbor_density = np.dot(prx_mat.values, st0_df["st0"].tolist())
    neighbor_density = pd.Series(data=neighbor_density, index=dscplist)
    dscp_density_sum = prx_mat.sum(axis=0)
    neighbor_density = neighbor_density.div(dscp_density_sum)
    neighbor_density = pd.Series(data=neighbor_density, name="Density")
    neighbor_density.index.name = 'DIS'
    neighbor_density = neighbor_density.reset_index()
    exp_df = neighbor_density.merge(st0_df, left_on="DIS", right_index=True)
    exp_df = exp_df.merge(st1_df, left_on="DIS", right_index=True)
    #exp_df = pd.concat([neighbor_density, st0_df, st1_df], axis=1)

    return exp_df


def struct_prx(prx_mat, dscplist):
    """pivot the proximity data to a matrix shape
    reorder the row and columns"""
    prx_mat = prx_mat.pivot(index="source", columns="target", values="weight")
    # set the self similarity as 0
    np.fill_diagonal(prx_mat.values, 0)
    prx_mat = prx_mat.reindex(dscplist)
    prx_mat = prx_mat[dscplist]
    return prx_mat


def cal_trans(rca_df, prx_mat, periods):
    """calculate transition probability by each country between the current
    step st0 and the next step st1."""
    density_df = pd.DataFrame()

    # do it for each country
    for cntry in cntrylist:
        cntry_df = rca_df[rca_df.COUNTRY == cntry]
        for ind_st0 in range(len(periods) - 1):
            st0_df = cntry_df[cntry_df.YEAR == periods[ind_st0]]
            st1_df = cntry_df[cntry_df.YEAR == periods[ind_st0 + 1]]
            if not st0_df.empty and not st1_df.empty:
                st0_df = extract_time_signal(st0_df, dscplist, "st0")
                st1_df = extract_time_signal(st1_df, dscplist, "st1")
                exp_df = cal_exp(cntry_df, st0_df, st1_df, prx_mat, dscplist)
                exp_df['COUNTRY'] = cntry
                exp_df['CRRT_TIME'] = periods[ind_st0]
                density_df = pd.concat([density_df, exp_df])
    return density_df


if __name__ == "__main__":
    RCA_FILE = sys.argv[1]
    PROX_FILE = sys.argv[2]
    TRANS_FILE = sys.argv[3]

    rca_df = pd.read_csv(RCA_FILE, header=0, names=['COUNTRY', 'DIS', 'RCA', 'YEAR', 'ST'])
    rca_df = assign_sig(rca_df)
    cntrylist = rca_df.COUNTRY.unique()
    dscplist = rca_df.DIS.unique()
    

    prx_mat = pd.read_csv(
        PROX_FILE, header=None, sep="\t", names=["source", "target", "weight"]
    )
    prx_mat = struct_prx(prx_mat, dscplist)

    START_YRS = list(range(1973, 2018, 5))
    END_YRS = list(range(1977, 2018, 5))
    PERIODS = ['{}-{}'.format(sy, ey) for sy, ey in zip(START_YRS, END_YRS)]    

    density_df = cal_trans(rca_df, prx_mat, PERIODS)
    density_df.to_csv(TRANS_FILE, index=False)
