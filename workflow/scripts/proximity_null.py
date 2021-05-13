import sys
from collections import Counter

import numpy as np
import pandas as pd

DENSITY_FILE = sys.argv[1]
PARAMS_FILE = sys.argv[2]
YEAR_INTERVAL_FILE = sys.argv[3]
OUTPUT_FILE = sys.argv[4]

density_df = pd.read_csv(DENSITY_FILE)
params_df = pd.read_csv(PARAMS_FILE)
yearlist = []
with open(YEAR_INTERVAL_FILE) as f:
    for line in f.readlines():
        yearlist.append(line.strip("\n"))
cntrylist = density_df.COUNTRY.unique().tolist()


def assign_prob(ddata, params_df, incomegroup='ALL'):
    params = params_df.set_index(["INCOME_GROUP", "START_STATE"]).to_dict(
            orient="index")

    dis2adv = params[("ALL", 0)]
    adv2dis = params[("ALL", 1)]

    def return_prob(density, st0flag):
        if st0flag == 0:
            prob = dis2adv['CONSTANT'] + (dis2adv['SLOPE'] * density)
        else:
            prob = adv2dis['CONSTANT'] + (adv2dis['SLOPE'] * density)

        prob = max(0, prob)
        return prob

    data = ddata.copy()
    data["prob"] = data[["Density", "st0"]].apply(
        lambda x: return_prob(x["Density"], x["st0"]), axis=1
    )
    return data


def get_numchange(data, t0flag, t1flag):
    num = data[(data.st0 == t0flag) & (data.st1 == t1flag)].shape[0]
    return num


def get_nextprofileprob(ddata, advdict, disdict, t1):
    profile_pred = ddata[["DIS", "st0", "COUNTRY"]].copy()
    for key, value in advdict.items():
        profile_pred.loc[profile_pred["DIS"] == key, "st0"] = value
    for key, value in disdict.items():
        profile_pred.loc[profile_pred["DIS"] == key, "st0"] = 1 - value
    profile_pred["CRRT_TIME"] = t1
    return profile_pred


def pred_byprob(ddata, t0flag, num):
    data = ddata[ddata.st0 == t0flag].copy()
    sum = data["prob"].sum()
    data["prob_norm"] = data["prob"] / sum
    dislist = data.DIS.tolist()
    prob = data.prob_norm.tolist()
    n = 100  # the number of times to do the sampling
    selectlist = []
    for s in np.arange(n):
        sample = np.random.choice(dislist, size=num, replace=False, p=prob)
        selectlist.extend(sample)
    selectdict = {k: v / n for k, v in Counter(selectlist).items()}
    return selectdict


prob_df = assign_prob(density_df, params_df)
final_prob = pd.DataFrame()
for cntry in cntrylist:
    cntry_filter = prob_df[prob_df.COUNTRY == cntry]
    for index, t0 in enumerate(yearlist[:-1]):
        t1 = yearlist[index + 1]
        profile_t0 = cntry_filter[cntry_filter.CRRT_TIME == t0]
        if not profile_t0.empty:
            delta_adv = get_numchange(profile_t0, 0, 1)
            delta_dis = get_numchange(profile_t0, 1, 0)
            advlist = pred_byprob(profile_t0, 0, delta_adv)
            dislist = pred_byprob(profile_t0, 1, delta_dis)
            profile_pred = get_nextprofileprob(profile_t0, advlist, dislist, t1)
            final_prob = pd.concat([final_prob, profile_pred])

final_prob.to_csv(OUTPUT_FILE, index=False)
