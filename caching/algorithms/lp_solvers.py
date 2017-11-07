# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Primal dual interior method
# **********************************************************************************#
from __future__ import division
import numpy as np
from cvxopt import matrix, solvers


def primal_dual_interior_method(variables, theta_est_bk, *args, **kwargs):
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
