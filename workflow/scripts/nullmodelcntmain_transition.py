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

cntry_group = pd.read_csv(CNTRY_GROUP)
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
    for period in time_interval:
        cntry_period_density = density_df[(density_df.COUNTRY == cntry) & (density_df.CRRT_TIME == period)]
        if not cntry_period_density.empty:
            cntry_period_prob = trmodule.cal_prob(cntry_period_density,adv_intcpt, adv_slope, dis_intcpt, dis_slope)
            cntry_main_group = cntry_group[(cntry_group.COUNTRY == cntry) & (cntry_group.YEAR==period)]['GROUP_ADV'].values[0]
            act_adv = trmodule.get_actnum_ingroup(cntry_period_prob, 0, 1, cntry, period)
            exp_adv = trmodule.get_expnum_ingroup_cntmain(cntry_period_prob, act_adv, 0, cntry_main_group, cntry, period, dscp_group)
            cntry_period_adv = pd.concat([act_adv, exp_adv],ignore_index=True)
            adv_result_df = pd.concat([adv_result_df, cntry_period_adv], ignore_index=True)
            

            act_dis = trmodule.get_actnum_ingroup(cntry_period_prob, 1, 0, cntry, period)
            exp_dis = trmodule.get_expnum_ingroup_cntmain(cntry_period_prob, act_dis, 1, cntry_main_group, cntry, period, dscp_group)
            cntry_period_dis = pd.concat([act_dis, exp_dis],ignore_index=True)
            dis_result_df = pd.concat([dis_result_df, cntry_period_dis], ignore_index=True)
adv_result_df.to_csv(ADV_RESULT_FILE, index=False)
dis_result_df.to_csv(DIS_RESULT_FILE, index=False)