"""this script constructs a null model of discipline development based 
on the probability calculated from the density"""

import pandas as pd
import numpy as np
import copy
import random
import sys
import trans_module as trmodule

 
DENSITY_FILE = sys.argv[1]
DSCP_GROUP_FILE = sys.argv[2]
CNTRY_GROUP = sys.argv[3]
PARAMS_FILE = sys.argv[4]
ADV_RESULT_FILE = sys.argv[5]
DIS_RESULT_FILE = sys.argv[6]

density_df = pd.read_csv(DENSITY_FILE)
dscp_group = pd.read_csv(DSCP_GROUP_FILE, sep="\t", names=["DIS", "DIS_GROUP"])

density_df = density_df.merge(dscp_group, left_on="DIS", right_on="DIS")

params = pd.read_csv(PARAMS_FILE, index_col=0)
adv_intcpt = params.loc['activation']['intercept']
adv_slope =  params.loc['activation']['slope']
dis_intcpt = params.loc['inactivation']['intercept']
dis_slope = params.loc['inactivation']['slope']


cntrylist = density_df.COUNTRY.unique()
time_interval = density_df.CRRT_TIME.unique()
adv_result_df = pd.DataFrame()
dis_result_df = pd.DataFrame()

for cntry in cntrylist:
    for time in time_interval:
        cntry_time_density = density_df[(density_df.COUNTRY == cntry) & (density_df.CRRT_TIME == time)]
        if not cntry_time_density.empty:
            cntry_time_prob = trmodule.cal_prob(cntry_time_density,adv_intcpt, adv_slope, dis_intcpt, dis_slope)
            act_adv = trmodule.get_actnum_ingroup(cntry_time_prob, 0, 1, cntry, time)
            exp_adv = trmodule.get_expnum_ingroup(cntry_time_prob, act_adv, 0, cntry, time, dscp_group)
            adv_result_df = pd.concat([adv_result_df, act_adv, exp_adv])

            act_dis = trmodule.get_actnum_ingroup(cntry_time_prob, 1, 0, cntry, time)
            exp_dis = trmodule.get_expnum_ingroup(cntry_time_prob, act_dis, 1, cntry, time, dscp_group)
            dis_result_df = pd.concat([dis_result_df, act_dis, exp_dis])

adv_result_df.to_csv(ADV_RESULT_FILE, index=False)
dis_result_df.to_csv(DIS_RESULT_FILE, index=False)