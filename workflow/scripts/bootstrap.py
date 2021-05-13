import numpy as np
import pandas as pd


def bootstrap(population, stat_func, resample=simple_resample, n_ensemble=10):
    n = len(population)
    xlist = []
    ylist = []
    for _ in range(n_ensemble):
        x, y = stat_func(population[resample(n)])
        xlist = xlist + x
        ylist = ylist + y
    return xlist, ylist


def theta1_coef(data_array, flagt0, colname):
    """Computes the slope using a bootstrapped sample of the data:
    (disci,status_at_t0,status_at_t1).


    This function aggregates data points belong to the same bin and calculates
    the probability of making the transition. The transition is either
    from adv -> not_adv or not_adv -> adv.

    Parameters
    ----------
    data_array : N x 3 array
        the input data array is N by 3, where N is the number of observations.
        The first column contains the status at t0 and the second one contains
        that at t1. The third column is the density bin.

    flagt0 : 0 or 1
        The initial status that we care about. 0 means not having relative
        advantage in the discipline. 1 means having relative advantage.

    colname : A string "fail" or "suc"
        "fail" means we want to see the final status of relative disadvantage.

    Returns
    -------
    a tuple of two lists
        The first list ...
        The second list ...
    """

    sample_df = pd.DataFrame(data_array, columns=["st0", "st1", "bin"])
    df = sample_df[sample_df.st0 == flagt0]

    # for each bin, there will be either st1=0 or st1=1. this counts how many
    # transitions into either state.
    df = df.groupby(["bin", "st1"]).size().reset_index(name="num")
    df = df.pivot(index="bin", columns="st1", values="num")
    df.columns = ["fail", "suc"]
    df = df.div(df.sum(axis=1), axis=0).reset_index()
    df[["fail", "suc"]] = df[["fail", "suc"]].fillna(value=0)
    df = df[(df.fail != 0) & (df.suc != 0)]
    x = df["binned"].values.tolist()
    y = df[colname].values.tolist()

    return x, y


def get_bar_values(data_df):
    """
    """
    data_df = data_df.groupby("binned")["fail"].apply(list).reset_index()
    data_df["mean"] = data_df["fail"].apply(lambda x: np.mean(x))
    data_df["std"] = data_df["fail"].apply(lambda x: np.std(x))
    x = data_df.binned.values
    y = data_df["mean"].values
    error = data_df["std"].values
    return x, y, error
