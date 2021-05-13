# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 2017
Module:
    nestedness_calculator.py
Author:
    Mika Straka
Description:
    Calculator of the nestedness of binary biadjacency matrices.
    Implemented algorithms are:
        - NODF (Nestedness based on Overlap and Decreasing Fill) [AlmeidaNeto]_
Usage:
    Be ``mat`` a two-dimensional binary NumPy array. The nodes of the two
    bipartite layers are ordered along the rows and columns, respectively.
    The NODF nestedness can be calculated directly without initializing a
    class instance::
        >>> from nestedness_calculator import NestednessCalculator
        >>> nodf_score = NestednessCalculator(mat).nodf(mat)
    When calling ``NestednessCalculator(mat)``, the matrix is tested for
    binarity. Furthermore, if one or more columns or rows consist only of zeros,
    the program aborts.
References:
.. [AlmeidaNeto] `M. Almeida-Neto, P. Guimareas, P. R. Guimaraes, R. D Loyala,
    W. Ulrich, A consistent metric for nestedness analysis in ecological
    systems: reconciling concept and measurement, Oikos 117: 1227-1239 (2008),
    <http://dx.doi.org/10.1111/j.0030-1299.2008.16644.x>`_
"""

import numpy as np


class NestednessCalculator(object):
    """Calculates the nestedness of the input matrix.
    The algorithms that have been implemented are:
        - NODF (Nestedness based on Overlap and Decreasing Fill)
    """
    def __init__(self, mat):
        """Initialize the Nestedness calculator and check the input matrix.
        :param mat: binary input matrix
        :type mat: numpy.array
        """
        self.check_input_matrix_is_binary(mat)
        self.check_degrees(mat)

    @staticmethod
    def check_input_matrix_is_binary(mat):
        """Check that the input matrix is binary, i.e. entries are 0 or 1.
        :param mat: binary input matrix
        :type mat: numpy.array
        :raise AssertionError: raise an error if the input matrix is not
            binary
        """
        assert np.all(np.logical_or(mat == 0, mat == 1)), \
            "Input matrix is not binary."

    @staticmethod
    def check_degrees(mat):
        """Check that rows and columns are not completely zero.
        :param mat: binary input matrix
        :type mat: numpy.array
        :raise AssertionError: raise an error if the input matrix has
            completely zero rows or columns.
        """
        assert np.all(mat.sum(axis=1) != 0), \
            "Input matrix rows with only zeros, abort."
        assert np.all(mat.sum(axis=0) != 0), \
            "Input matrix columns with only zeros, abort."

################################################################################
# NODF - Nestedness based on Overlap and Decreasing Fill
################################################################################

    def get_paired_nestedness(self, mat, rows=True):
        """Calculate the paired nestedness along the rows or columns of the.
        :param mat: binary input matrix
        :type mat: numpy.array
        :param rows: if True, pairs are calculated along the rows, if False
            along the columns
        :type rows: bool
        :returns: degree of paired nestedness
        :rtype: float
        The method uses the algorithm described in the `BiMat framework for
        MATLAB <https://bimat.github.io/alg/nestedness.html>`_.
        """
        if rows:
            # consider rows
            po_mat = np.dot(mat, mat.T)
            degrees = mat.sum(axis=1)
        else:
            # consider cols
            po_mat = np.dot(mat.T, mat)
            degrees = mat.sum(axis=0)
        assert len(degrees) == len(po_mat)

        neg_delta = (degrees != degrees[:, np.newaxis])
        deg_matrix = degrees * np.ones_like(po_mat)
        deg_minima = np.minimum(deg_matrix, deg_matrix.T)
        n_pairs = po_mat[neg_delta] / (2. * deg_minima[neg_delta])
        return n_pairs.sum()

    def nodf(self, mat):
        """Calculate the NODF nestedness of the input matrix [AlmeidaNeto]_.
        :param mat: binary input matrix
        :type mat: numpy.array
        :returns: NODF nestedness of the input matrix
        :rtype: float
        The algorithm has been tested by comparison with the `online tool
        provided at <http://ecosoft.alwaysdata.net/>`_
        """
        n_pairs_rows = self.get_paired_nestedness(mat, rows=True)
        n_pairs_cols = self.get_paired_nestedness(mat, rows=False)
        norm = np.sum(np.array(mat.shape) * (np.array(mat.shape) - 1) / 2.)
        nodf = (n_pairs_rows + n_pairs_cols) / norm
        return nodf
