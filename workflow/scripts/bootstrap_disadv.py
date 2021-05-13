import numpy as np
import pandas as pd


def simple_resample(n):
    return np.random.randint(low=0, high=n, size=n)


def bootstrap(boot_pop, statistic,resample=simple_resample, replicates = 20):
    n = len(boot_pop)
    # thetalist = []
    # constantlist=[]
    # sample_df = pd.DataFrame()
    xlist = []
    ylist = []
    for _ in range(replicates):
        x, y = statistic(boot_pop[resample(n)])
        xlist = xlist + x
        ylist = ylist + y
        # constantlist.append(params[0])
        # thetalist.append(params[1])
        # sample_df = pd.concat([sample_df, boot_df])

    return xlist, ylist


def theta1_coef(data_array):

    sample_df = pd.DataFrame(data_array, columns=["st0", "st1", "binned"])
    fail_df = sample_df[sample_df.st0 == 1]
    fail_df = fail_df.groupby(["binned", "st1"]).size().reset_index(name="num")
    fail_df = fail_df.pivot(index="binned", columns="st1", values="num")
    fail_df.columns = ["fail", "suc"]
    fail_df = fail_df.div(fail_df.sum(axis=1), axis=0).reset_index()
    fail_df[["fail", "suc"]] = fail_df[["fail", "suc"]].fillna(value=0)
    fail_df = fail_df[(fail_df.fail != 0) & (fail_df.suc != 0)]
    x = fail_df["binned"].values.tolist()
    y = fail_df["fail"].values.tolist()

    return x, y


def get_bar_values(data_df):
    data_df = data_df.groupby("binned")["fail"].apply(list).reset_index()
    data_df["mean"] = data_df["fail"].apply(lambda x: np.mean(x))
    data_df["std"] = data_df["fail"].apply(lambda x: np.std(x))
    x = data_df.binned.values
    y = data_df["mean"].values
    error = data_df["std"].values
    return x, y, error
