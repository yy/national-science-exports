"""functions to calculate discipline transitions
"""
import pandas as pd
import numpy as np
import copy
import random

def cal_prob(density_df, adv_intcpt, adv_slope, dis_intcpt, dis_slope):
    """calculate the transform probability from density
    """

    def p_adv(density):
        prob = adv_intcpt+adv_slope*density
        return prob
    def p_dis(density):
        prob = dis_intcpt+(dis_slope)*density
        return prob
    density_df['PROB'] = density_df[['Density', 'st0']].apply(
        lambda x: p_adv(x['Density']) if x['st0']==0 else p_dis(x['Density']), axis=1)
    density_df['PROB'] = density_df['PROB'].apply(lambda x:max(x,0))
    return density_df

def norm_prob(population_df):
    population_df['PROB_NORM'] = population_df['PROB'].div(
        population_df['PROB'].sum(),axis=0)
    return population_df

def get_actnum_ingroup(cntry_density, t0_flag, t1_flag, cntry, time):
    """get the actual number of change within group
    t0_flag: whether the discipline is activated at time t
    t1_flag: whether the discipline is activated at time t+1
    """
    changed_df = cntry_density[(cntry_density.st0==t0_flag) & (cntry_density.st1==t1_flag)]
    changed_df = changed_df.groupby(["DIS_GROUP"]).size()
    changed_df = changed_df.reindex(['NM','NE','SHM'])
    changed_df = changed_df.fillna(0)
    changed_df = pd.DataFrame(changed_df, columns=['NUM_CHANGE']).reset_index()
    changed_df['COUNTRY'] = cntry
    changed_df['PERIOD'] = time
    changed_df['SOURCE'] = 'actual'
    return changed_df

def get_expnum_ingroup(cntry_prob, act_changed, t0_flag, cntry, time, dscp_group):
    sampled_exp_list = []
    population_df = cntry_prob[cntry_prob.st0==t0_flag]
    population_df = norm_prob(population_df)
    sample_num = act_changed['NUM_CHANGE'].sum()
    iternum = 20
    population_list = population_df['DIS'].values
    prob = population_df['PROB_NORM'].values
    
    for i in range(iternum):
        s = np.random.choice(population_list, size=int(sample_num), p=prob, replace=False)
        sampled_exp_list.extend(s)
    sampled_exp_df = pd.DataFrame(
        sampled_exp_list, columns=["DIS"]).merge(dscp_group, left_on="DIS", right_on="DIS").groupby(['DIS_GROUP']).size()
    sampled_exp_df = sampled_exp_df/iternum
    sampled_exp_df = sampled_exp_df.reindex(['NM','NE','SHM']).fillna(0)
    sampled_exp_df = pd.DataFrame(sampled_exp_df, columns=['NUM_CHANGE']).reset_index()
    sampled_exp_df['COUNTRY'] = cntry
    sampled_exp_df['PERIOD'] = time
    sampled_exp_df['SOURCE'] = 'exp'
    return sampled_exp_df

def get_expnum_ingroup_cntmain(cntry_prob, act_changed, t0_flag, cntry_main_group, cntry, period, dscp_group):
    exp_list = []
    main_group_num = act_changed.loc[(act_changed.DIS_GROUP == cntry_main_group), 'NUM_CHANGE'].values[0]
    population_df = cntry_prob[cntry_prob.st0==t0_flag]
    population_filtered_df = population_df[population_df.DIS_GROUP != cntry_main_group]
    population_filtered_df = norm_prob(population_filtered_df)
    sample_num = act_changed['NUM_CHANGE'].sum() - main_group_num
    iternum = 20
    population_list = population_filtered_df['DIS'].values
    prob = population_filtered_df['PROB_NORM'].values
    
    if sample_num>0:
        for i in range(iternum):
            s = np.random.choice(population_list, size=int(sample_num), p=prob, replace=False)
            exp_list.extend(s)     
    exp_df = pd.DataFrame(
        exp_list,columns=["DIS"]).merge(dscp_group, left_on="DIS", right_on="DIS").groupby(["DIS_GROUP"]).size()
    exp_df = exp_df/iternum
    exp_df = pd.DataFrame(exp_df, columns=['NUM_CHANGE']).reset_index()
    exp_df = exp_df.append({'DIS_GROUP':cntry_main_group, 'NUM_CHANGE':main_group_num}, ignore_index=True)
    exp_df = exp_df.set_index('DIS_GROUP').reindex(['NM','NE','SHM']).reset_index()
    exp_df = exp_df.fillna(0)
    exp_df['COUNTRY'] = cntry
    exp_df['PERIOD'] = period
    exp_df['SOURCE'] = 'exp'
    return exp_df
    