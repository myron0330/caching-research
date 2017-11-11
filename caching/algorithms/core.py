# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Core algorithms
# **********************************************************************************#
import numpy as np
from itertools import product
from . lp_solvers import primal_dual_interior_method, solvers, matrix
from . recover import recover_from_


def _normalize_(result):
    """
    Normalize result

    Args:
        result(numpy.ndarray): matrix like
    """
    x_axis = xrange(result.shape[0])
    y_axis = xrange(result.shape[1])
    for (row, column) in product(x_axis, y_axis):
        if result[row, column] < 1e-3:
            result[row, column] = 0
        if result[row, column] > 0.99:
            result[row, column] = 1
    return result


def primal_dual_recover(variables, theta_est_bk, recover=True, lp_method=None, *args, **kwargs):
    """
    Using primal dual interior method to solve the relaxing problem, recover with knapsack dynamic programming.

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
        lp_method(function): which lp method to use
        recover(boolean): whether to recover the algorithm
    """
    lp_method = lp_method or primal_dual_interior_method
    solution = np.array(lp_method(variables, theta_est_bk)['x'])
    c_inv_bk = solution.reshape((variables.bs_number + 1, variables.file_number))
    c_bk = (1 - c_inv_bk)[:-1, :]
    if recover:
        return recover_from_(variables, c_bk)
    else:
        return c_bk


def primal_dual_with_candidate(variables, theta_est_bk, candidate, *args, **kwargs):
    """
    Primal dual interior method with candidate

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
        candidate(list): candidate solvers
    """
    candidate = map(lambda x: 1 - x, candidate)
    s_k = np.array(variables.sizes)
    u_bk = np.ones((variables.bs_number, variables.file_number)) * variables.user_size
    s_bk = np.array([variables.sizes]).repeat(variables.bs_number, axis=0)
    t_u_s_bk = theta_est_bk * u_bk * s_bk
    c_c_bk = t_u_s_bk / variables.v_bb
    c_x_bk = (t_u_s_bk / variables.v_cb - t_u_s_bk / variables.v_bb).sum(axis=0).reshape((1, t_u_s_bk.shape[1]))
    cvx_object_c = np.concatenate([c_c_bk, c_x_bk]).reshape(c_c_bk.size + c_x_bk.size)
    cvx_st_g = \
        np.zeros(shape=(cvx_object_c.size, variables.bs_number + variables.file_number * 2 + cvx_object_c.size * 2))
    cvx_st_h = np.zeros(variables.bs_number + variables.file_number * 2 + cvx_object_c.size * 2)
    _offset = 0
    for bs in xrange(variables.bs_number):
        row = xrange(bs * variables.file_number, (bs + 1) * variables.file_number)
        column = bs + _offset
        cvx_st_g[row, column] = -1 * s_k
        cvx_st_h[column] = variables.bs_memory - s_k.sum()
    _offset += variables.bs_number
    for k in xrange(variables.file_number):
        row = xrange(k, k + cvx_object_c.size, variables.file_number)
        column = k + _offset
        cvx_st_g[row, column] = [1] * (len(row) - 1) + [-1]
        cvx_st_h[column] = variables.bs_number - 1
    _offset += variables.file_number
    for k in xrange(variables.file_number):
        row = xrange(k, k + cvx_object_c.size, variables.file_number)
        column = k + _offset
        cvx_st_g[row, column] = [-1] * (len(row) - 1) + [variables.bs_number]
        cvx_st_h[column] = 0
    _offset += variables.file_number
    cvx_st_g[:, _offset: _offset + cvx_object_c.size] = np.identity(cvx_object_c.size)
    cvx_st_h[_offset: _offset + cvx_object_c.size] = 1
    _offset += cvx_object_c.size
    cvx_st_g[:, _offset:] = -1 * np.identity(cvx_object_c.size)
    cvx_st_h[_offset:] = 0
    # adjust with candidate and solve the problem
    adj_c = cvx_object_c[len(candidate):]
    adj_g = cvx_st_g[len(candidate):, :]
    minus_item = cvx_st_g[:len(candidate)] * np.array([candidate]).T
    minus_summation = minus_item.sum(axis=0)
    adj_h = cvx_st_h - minus_summation
    c, g, h = matrix(adj_c), matrix(adj_g.T), matrix(adj_h)
    solution = solvers.lp(c, g, h)
    solution = np.array(candidate + list(solution['x'])).reshape((variables.bs_number + 1, variables.file_number))
    c_bkt = 1 - solution
    assert isinstance(c_bkt, np.ndarray)
    c_bkt = _normalize_(c_bkt)
    return c_bkt
