""" test for core.py """

import pytest
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

import nsp.core


def test_gini():
    """ gini coefficient test """
    for _ in range(10):
        x = np.random.rand(500)
        assert nsp.core.gini_alt(x) == pytest.approx(nsp.core.gini_coef(x))

def test_bipartite_modularity():
    rcatest=[[0,1,0,0],[0,1,0,0],[1,1,1,0],[0,0,1,1],[1,0,0,1]]
    rcatest=pd.DataFrame(rcatest, index=[1,2,3,4,5],columns=['a','b','c','d'])
    indexgroup=[[1,1],[2,1],[3,1],[4,2],[5,2]]
    indexgroup=pd.DataFrame(indexgroup,columns=['index','group'])
    colgroup=[['a',1],['b',1],['c',2],['d',2]]
    colgroup=pd.DataFrame(colgroup,columns=['col','group'])
    assert nsp.core.bipart_modularity(rcatest,indexgroup,colgroup) == pytest.approx(22/81)


def test_rca_1():
    """ construct the first test for rca code """
    df = pd.DataFrame(
        np.array(
            [
                ["U", "U", "U", "U", "C", "C", "C"],
                ["a", "b", "c", "c", "a", "b", "a"],
                [10, 10, 10, 10, 10, 10, 10],
            ]
        ).T,
        columns=["COUNTRY", "SPECIALTY", "PAPER_CNT"],
    )
    df[["PAPER_CNT"]] = df[["PAPER_CNT"]].astype(int)

    dis_dict = df.groupby(["SPECIALTY"]).sum()  # number of pub in each discipline
    country_dict = df.groupby(["COUNTRY"]).sum()  # number of pub in each country
    pub_total = df["PAPER_CNT"].sum()
    df = df.groupby(["COUNTRY", "SPECIALTY"]).sum().reset_index()
    df = df.pivot(
        index="COUNTRY", columns="SPECIALTY", values="PAPER_CNT"
    )  # index is countryname column is discipline
    df = df.fillna(0.0)
    rca = nsp.core.cal_rca(country_dict, dis_dict, pub_total, df)

    # manually derived result
    rcatest = pd.DataFrame(
        np.array([[7 / 12, 7 / 8, 7 / 4], [14 / 9, 7 / 6, 0]]),
        columns=["a", "b", "c"],
        index=["U", "C"],
    )

    assert_frame_equal(rca, rcatest, check_names=False, check_like=True)


def test_rca_2():
    """ construct the first test for rca code """
    df = pd.DataFrame(
        np.array(
            [
                ["U", "U", "U", "U", "C", "C", "C"],
                ["a", "b", "c", "c", "a", "b", "a"],
                [0, 0, 10, 10, 10, 10, 10],
            ]
        ).T,
        columns=["COUNTRY", "SPECIALTY", "PAPER_CNT"],
    )
    df[["PAPER_CNT"]] = df[["PAPER_CNT"]].astype(int)

    dis_dict = df.groupby(["SPECIALTY"]).sum()  # number of pub in each discipline
    country_dict = df.groupby(["COUNTRY"]).sum()  # number of pub in each country
    pub_total = df["PAPER_CNT"].sum()
    df = df.groupby(["COUNTRY", "SPECIALTY"]).sum().reset_index()
    df = df.pivot(
        index="COUNTRY", columns="SPECIALTY", values="PAPER_CNT"
    )  # index is countryname column is discipline
    df = df.fillna(0.0)
    rca = nsp.core.cal_rca(country_dict, dis_dict, pub_total, df)

    # manually derived result
    rcatest = pd.DataFrame(
        np.array([[0, 0, 5 / 2], [5 / 3, 5 / 3, 0]]),
        columns=["a", "b", "c"],
        index=["U", "C"],
    )

    assert_frame_equal(rca, rcatest, check_names=False, check_like=True)
