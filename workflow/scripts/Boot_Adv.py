import numpy as np
import pandas as pd


def simple_resample(n):
    return np.random.randint(low=0, high=n, size=n)


def bootstrap(boot_pop, statistic,flagt0, colname, resample=simple_resample, replicates = 20):

    n = len(boot_pop)
    # thetalist = []
    # constantlist=[]
    # sample_df = pd.DataFrame()
    xlist = []
    ylist = []
    for _ in range(replicates):
        x, y = statistic(boot_pop[resample(n)], flagt0, colname)
        xlist = xlist + x
        ylist = ylist + y
    return xlist, ylist


def theta1_coef(data_array, flagt0, colname):

    sample_df = pd.DataFrame(data_array, columns=["st0", "st1", "binned"])
    suc_df = sample_df[sample_df.st0 == flagt0]
    suc_df = suc_df.groupby(["binned", "st1"]).size().reset_index(name="num")
    suc_df = suc_df.pivot(index="binned", columns="st1", values="num")
    suc_df.columns = ["fail", "suc"]
    suc_df = suc_df.div(suc_df.sum(axis=1), axis=0).reset_index()
    suc_df[["fail", "suc"]] = suc_df[["fail", "suc"]].fillna(value=0)
    suc_df = suc_df[(suc_df.fail != 0) & (suc_df.suc != 0)]
    x = suc_df["binned"].values.tolist()
    y = suc_df[colname].values.tolist()

    return x, y


def get_bar_values(data_df):
    data_df = data_df.groupby("binned")["suc"].apply(list).reset_index()
    data_df["mean"] = data_df["suc"].apply(lambda x: np.mean(x))
    data_df["std"] = data_df["suc"].apply(lambda x: np.std(x))
    x = data_df.binned.values
    y = data_df["mean"].values
    error = data_df["std"].values
    return x, y, error
