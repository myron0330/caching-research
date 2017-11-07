# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Core algorithms
# **********************************************************************************#
import numpy as np
from . lp_solvers import primal_dual_interior_method
from . recover import recover_from_


def primal_dual_recover(variables, theta_est_bk, recover=True, *args, **kwargs):
    """
    Using primal dual interior method to solve the relaxing problem, recover with knapsack dynamic programming.

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
        recover(boolean): whether to recover the algorithm
    """
    solution = np.array(primal_dual_interior_method(variables, theta_est_bk)['x'])
    c_inv_bk = solution.reshape((variables.bs_number + 1, variables.file_number))
    c_bk = (1 - c_inv_bk)[:-1, :]
    if recover:
        return recover_from_(variables, c_bk)
    else:
        return c_bk


def lp_solvers(variables, theta_est_bk, candidate, *args, **kwargs):
    """
    Primal dual interior method

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
    """
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
        row = xrange(bs * variables.file_number, bs * variables.file_number + variables.file_number)
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
    c, g, h = matrix(cvx_object_c), matrix(cvx_st_g.T), matrix(cvx_st_h)
    solution = solvers.lp(c, g, h)
    return solution
