""" core utils for the project """
import os
from collections import Counter
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

""" Gini """


def gini_coef(alist):
    """ Gini Coefficient """
    cum_x = np.cumsum(sorted(np.append(alist, 0)))
    sum_x = cum_x[-1]
    xarray = np.array(range(0, len(cum_x))) / np.float(len(cum_x) - 1)
    yarray = cum_x / sum_x
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A + B)


def gini_alt(alist):
    """ Another implementation to calcualte Gini coefficient.

    Source:
    https://stackoverflow.com/questions/39512260/calculating-gini-coefficient-in-python-numpy

    """

    # Mean absolute difference
    mad = np.abs(np.subtract.outer(alist, alist)).mean()
    # Relative mean absolute difference
    rmad = mad / np.mean(alist)
    # Gini coefficient
    return 0.5 * rmad


""" pub record utilities """


def extract_pubrec_by_timeperiod(pubrec_file, start_year, end_year):
    """ load the publication record file and then return a dataframe that
    contains only the record between (start_year, end_year).

    It is inclusive. i.e. start_year <= record year <= end_year
    """
    pubrec_df = pd.read_csv(pubrec_file, dtype={"PAPER_CNT": float, "YEAR": int})
    return pubrec_df[pubrec_df["YEAR"].between(start_year, end_year, inclusive=True)][
        ["COUNTRY", "SPECIALTY", "PAPER_CNT"]
    ]


def pubcnt_by_cntry_and_disc(pubrec_df):
    """ from the publication record file that contains rows of
    (country, discipline, year, pub count or amount), it produces a pivot table
    (matrix) where the rows are the countries, columns are disciplines, and the
    values are the number (amount) of publications for that (country, discipline)
    """
    cntry_dis_agg_df = pubrec_df.groupby(["COUNTRY", "SPECIALTY"]).sum().reset_index()
    numpubs_in_cntry_dis_df = cntry_dis_agg_df.pivot(
        index="COUNTRY", columns="SPECIALTY", values="PAPER_CNT"
    )
    return numpubs_in_cntry_dis_df.fillna(0.0)


def pubcnt_by_cntry_and_group(pubrec_df):
    """ from the publication record file that contains rows of
    (country, discipline, year, pub count), it produces a pivot table
    (matrix) where the rows are the countries, columns are groups, and the
    values are the number (amount) of publications for that (country, group)
    """
    cntry_dis_agg_df = pubrec_df.groupby(["COUNTRY", "GROUP"]).sum().reset_index()
    numpubs_in_cntry_dis_df = cntry_dis_agg_df.pivot(
        index="COUNTRY", columns="GROUP", values="PAPER_CNT"
    )
    return numpubs_in_cntry_dis_df.fillna(0.0)


def drop_all_countries_entry(pubrec_df):
    return pubrec_df[pubrec_df["COUNTRY"] != "ALL COUNTRIES"]


""" Proximity """


def cal_prox(df_rca):
    """calculate the proximity between each pair of disciplines, which is
    defined by the min( P(A|B), P(B|A) ).

    Parameters
    ----------
    df_rca : pandas DataFrame
        index is country and columns are disciplines, each value at
        (c, d) means the RCA for country c in discipline d.

    returns
    -------
    df_prox : pandas DataFrame
        both index and column is the list of all disciplines.

    """
    dis_list = df_rca.columns

    df_prox = pd.DataFrame(index=dis_list, columns=dis_list, dtype="float")
    df_prox = df_prox.fillna(0.0)
    np.fill_diagonal(df_prox.values, 1.0)

    # precompute the marginal value, the number of times rca is larger than 1
    n_adv_countries = {d: len(df_rca[df_rca[d] > 1.0]) for d in dis_list}

    for dis_i, dis_j in combinations(dis_list, 2):
        n_i = n_adv_countries[dis_i]
        n_j = n_adv_countries[dis_j]
        n_ij = len(df_rca[(df_rca[dis_i] > 1.0) & (df_rca[dis_j] > 1.0)])
        prox = n_ij / max(n_i, n_j)  # min((n_ij / n_i), (n_ij / n_j))

        df_prox.at[dis_i, dis_j] = prox
        df_prox.at[dis_j, dis_i] = prox

    return df_prox


""" RCA """


def cal_rca(country_dict, dis_dict, pub_total, df_data):
    """calculate rca value.
    """

    df_rca = pd.DataFrame().reindex_like(df_data).fillna(0.0)

    for country, cou_row in country_dict.iterrows():
        # total number of publication published by the country
        country_total = cou_row["PAPER_CNT"]

        for dis, dis_row in dis_dict.iterrows():
            # total number of publication published in that discipline
            dis_total = dis_row["PAPER_CNT"]

            # number of publication in that discipline of that country
            value = df_data.loc[country, dis]

            # try:
            # rca=(value/country_total)*(pub_total/dis_total)
            # except RuntimeWarning:
            # rca=0
            rca = (value / country_total) * (pub_total / dis_total)
            df_rca.at[country, dis] = rca

    return df_rca


def order_rca_matrix(rca_df, ascending_flag_dis=False, ascending_flag_cntry=True):
    """ rearrange the rca matrix for nestedness

    input:
        rca_df: RCA values for each country (row) and each discipline (column)

    returns:
        order_rca_df: disciplines and countries are ordered in descending order
                      in terms of the number of RCA>1 disciplines and the number
                      of RCA>1 countries respectively.

    """

    # sorting the columns (disciplines)
    num_highrca_cntry_per_dis = rca_df.gt(1.0).sum(axis=0)
    sorted_dis_list = list(
        num_highrca_cntry_per_dis.sort_values(ascending=ascending_flag_dis).index
    )
    ordered_rca_df = rca_df[sorted_dis_list]

    # sorting the rows (countries)
    num_highrca_dis_per_cntry = rca_df.gt(1.0).sum(axis=1)
    sorted_cntry_list = list(
        num_highrca_dis_per_cntry.sort_values(ascending=ascending_flag_cntry).index
    )
    ordered_rca_df = ordered_rca_df.reindex(sorted_cntry_list)

    return ordered_rca_df


""" Network """


def extract_backbone(G, alpha):
    """ network backbone extraction using the multi-scale backbone algorithm
    by Serrano et al., PNAS.

    source:
    https://gist.github.com/bagrow/11181518#file-extract_backbone-py

    """
    keep_graph = nx.Graph()
    for n in G:
        k_n = len(G[n])
        if k_n > 1:
            sum_w = G.degree(n, weight="weight")
            for nj in G[n]:
                pij = 1.0 * G[n][nj]["weight"] / sum_w
                if (1 - pij) ** (k_n - 1) < alpha:  # edge is significant
                    keep_graph.add_edge(n, nj, weight=G[n][nj]["weight"])
    return keep_graph


""" MISC utility functions """


def extract_years_from_path(file_path):
    """ extract two year values from the path assuming the following format:

    'aaa_bbbb_cc_{startyear}-{endyear}.ext'
    """
    basename = os.path.basename(file_path)
    name, ext = os.path.splitext(basename)
    return map(int, name.split("_")[-1].split("-"))


def get_mapping(file_path, k="ID", v="NODE"):
    """return a dict where key is the label of node and value is the id of node.
    """
    node_id_dict = pd.read_csv(file_path, sep="\t").set_index(k)[v].to_dict()
    return node_id_dict


"""Figures"""


def plot_worldmap(ax, fig, basemap, data_empty, data, plotcolumn, cmap, vmax=1):
    """plot a basemap and color the country based on the column passed into
    """

    basemap.plot(ax=ax, linewidth=0.25, edgecolor="#8C8C8C", facecolor="#ffffff")
    data_empty.plot(ax=ax, linewidth=0.25, facecolor="#c4c0c0")
    data.plot(column=plotcolumn, cmap=cmap, vmin=0, vmax=vmax, ax=ax)
    ax.axis("off")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=vmax))
    sm._A = []
    fig.colorbar(sm, cax=cax)
    return fig, ax


def split_full_df(df):
    all_country_df = df[df["COUNTRY"] == "ALL COUNTRIES"]
    pubrec_filtered_df = df[df["COUNTRY"] != "ALL COUNTRIES"]
    return all_country_df, pubrec_filtered_df


def get_sample_profile(pcnt_file, start, end):
    """return the data which would be used to draw the sample"""
    smple_pf_df = extract_pubrec_by_timeperiod(pcnt_file, start, end)
    if "full" in pcnt_file:
        smple_all, smple_pf_df = split_full_df(smple_pf_df)
    smple_pf_df = smple_pf_df.groupby(["COUNTRY", "SPECIALTY"]).sum().reset_index()
    smple_pf_df["PAPER_CNT"] = smple_pf_df["PAPER_CNT"].apply(lambda x: np.ceil(x))
    return smple_pf_df


def cstruct_smple_population(cntry_df):
    """create the population which would be used in the sampling"""
    dis_dict = cntry_df.set_index("SPECIALTY").to_dict()["PAPER_CNT"]
    population = [key for key, value in dis_dict.items() for i in range(int(value))]
    return population


def smple_and_avg(population, cntry_numpubs, dscplist, cal_fun, N):
    """sample the discipline from the population by cntry_numpubs times,
    normalized the sampled discipline profile by the actual numpubs_in_dis
    and calculate the indicator by the passed function cal_fun
    repeat the process over N times."""
    resultlist = []
    for i in range(N):
        sample = np.random.choice(population, cntry_numpubs, replace=True)
        sample_dis = Counter(sample)
        sample_dis_df = pd.Series(sample_dis)
        # sample_dis_norm_df = sample_dis_df.divide(numpubs_in_dis, fill_value=0)
        sample_dis_df = sample_dis_df.reindex(dscplist, fill_value=0)
        resultlist.append(cal_fun(sample_dis_df.values))
    avg_sample = np.average(resultlist)
    return avg_sample


def cal_save_btstrping(
    smple_pf_df, numpubs_in_cntry_df, dscplist, cal_fun, col_name, N
):
    """iterate over countries to calculate the indicator and
    save the result to file"""
    countrylist = numpubs_in_cntry_df.index.tolist()
    cntry_sample_avg = {}

    for country in countrylist:
        cntry_smple_profile = smple_pf_df[smple_pf_df.COUNTRY == country]
        population = cstruct_smple_population(cntry_smple_profile)
        if len(population) > 0:
            cntry_numpubs = numpubs_in_cntry_df.at[country, "PAPER_CNT"]
            avg_sample = smple_and_avg(population, cntry_numpubs, dscplist, cal_fun, N)
            cntry_sample_avg[country] = avg_sample
    cntry_sampledavg_df = pd.Series(cntry_sample_avg, name="gini")
    cntry_sampledavg_df.index.name = "country"
    cntry_sampledavg_df = cntry_sampledavg_df.reset_index()
    return cntry_sampledavg_df


def merge_others_lagging(data_df, colname):
    data_df.loc[data_df[colname] == "Others", colname] = "Lagging"
    return data_df


def bipart_modularity(rca_df, indexgroup, colgroup):
    """rca_df is the bipartite network saved in dataframe format, index and
    column are node sets of the network.
    indexgroup and colgroup are group classification of nodes
    the modularity calculation is based on
    https://journals-aps-org.proxyiub.uits.iu.edu/pre/abstract/10.1103/PhysRevE.76.066102
    """

    m = rca_df.sum().sum()
    index_degree = rca_df.sum(axis=1).values
    col_degree = rca_df.sum(axis=0).values
    p = np.outer(index_degree, col_degree)
    prob_df = pd.DataFrame(p, index=rca_df.index, columns=rca_df.columns)
    prob_df = prob_df / m
    b_df = rca_df - prob_df

    modu = 0
    groups = indexgroup.group.unique()
    for group in groups:
        subindex = indexgroup[indexgroup.group == group]["index"].tolist()
        subcol = colgroup[colgroup.group == group]["col"].tolist()
        modu += b_df.loc[subindex, subcol].sum().sum()
    return modu / m
