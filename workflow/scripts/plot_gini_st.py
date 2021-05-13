""" This script plots the gini value distribution over different
S&T groups .

input:
argv[1]: The csv file contains country names and its gini value for all the periods
argv[2]: The S&T file specifies S&T group for each country

output: the distribution plot
argv[3]: path where the plot should be saved

"""
import numpy as np
import pandas as pd
import nsp.core
import matplotlib.pyplot as plt
import sys
import seaborn as sns

def plot_gini_st(gini_merge_df):

    st_list = ["Advanced", "Proficient", "Developing", "Lagging", "Others"]
    st_color_dict = nsp.core.get_st_color()
    f, ax = plt.subplots()

    for st in st_list:
        data = gini_merge_df[gini_merge_df["stindex"]==st]["ginivalue"]
        color = st_color_dict[st]
        sns.distplot(data, label=st, hist=False, color=color)
    
    plt.legend(loc='best', fontsize="large", frameon=False)
    plt.xlabel("Gini of scientific products", fontsize="x-large")
    plt.ylabel("Density", fontsize="x-large")
    return ax



if __name__ == "__main__":
    GINI_FILE = sys.argv[1]
    ST_GROUP_FILE = sys.argv[2]
    PLOT_PATH = sys.argv[3]

    gini_df = pd.read_csv(
        GINI_FILE, header=0, names=["country", "ginivalue"], dtype={"ginivalue": np.float64}
    )

    st_group_df = pd.read_csv(
        ST_GROUP_FILE, delimiter="\t", header=None, names=["country", "stindex"]
    )
    
    # assign the st index to each country
    gini_merge_df = gini_df.merge(
        st_group_df, how="left", on="country"
        )

    ax = plot_gini_st(gini_merge_df)
    plt.savefig(PLOT_PATH, format="pdf")