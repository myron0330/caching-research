# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Branch and bound algorithm
# **********************************************************************************#
from __future__ import division
import numpy as np
from itertools import product
from cvxopt import matrix, solvers
from . core import primal_dual_recover, lp_solvers
from .. basic.rewards import calculate_rewards
from .. utils.tree_utils import BinaryTree


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


def _valid_solution(result):
    """
    Judge whether the result is valid solution

    Args:
          result(result): matrix like
    """
    c_bkt = result[:-1, :].reshape((result.shape[0] - 1) * result.shape[1])
    for value in c_bkt:
        if value not in [0., 1.]:
            return False
    return True


def _pruning_tree(candidate, variables):
    """
    Pruning formula

    Args:
        candidate: candidate list
        variables: variables
    """
    candidate_array = np.array(candidate)
    size_array = np.array(variables.sizes[:len(candidate)])
    if sum(candidate_array * size_array) > variables.bs_memory:
        return True
    return False


def _pruning_iterator(iterator, variables, height):
    """
    Pruning iterator

    Args:
        iterator(iter): iterator
        variables(obj): variables
        height(int): height of tree
    """
    candidates = list()
    for candidate in iterator:
        candidate_array = np.array(candidate)
        size_array = np.array(variables.sizes[:len(candidate)])
        if len(candidate) == height:
            if variables.bs_memory - sum(candidate_array * size_array) > min(variables.sizes):
                continue
        else:
            if variables.bs_memory - sum(candidate_array * size_array) < min(variables.sizes[len(candidate):]):
                continue
        if variables.bs_memory - (height - candidate.count(0)) * max(variables.sizes) > min(variables.sizes):
            continue
        candidates.append(candidate)
    return candidates


def _pruning_node(candidate):
    """
    Pruning node begin with candidate
    :param candidate:
    :return:
    """



def branch_and_bound(variables, theta_est_bk, d_bkt):
    """
    Branch and bound method

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta
        d_bkt(matrix): demands
    """
    c_bkt = primal_dual_recover(variables, theta_est_bk, recover=True)
    rewards = calculate_rewards(variables, c_bkt, d_bkt, aggregate=True)
    incumbent = (c_bkt, rewards)
    head = list()
    for _ in xrange(variables.bs_number):
        tree = BinaryTree()
        tree.generate(6)
        iterator = list(tree.iterator_with_(pruning_func=_pruning_tree, variables=variables))
        candidates = _pruning_iterator(iterator, variables, 6)
        while candidates:
            candidate = head + candidates.pop(0)
            candidate_inverse = map(lambda x: 1 - x, candidate)
            c_bkt_inverse = lp_solvers(variables, theta_est_bk, candidate=candidate_inverse, recover=True)
            c_bkt = 1 - c_bkt_inverse
            assert isinstance(c_bkt, np.ndarray)
            c_bkt = _normalize_(c_bkt)
            validation = _valid_solution(c_bkt)
            rewards = calculate_rewards(variables, c_bkt, d_bkt, aggregate=True)
            if rewards < incumbent[1]:
                _pruning_node(candidate)

        # # todo. branch and bound
    # s_k = np.array(variables.sizes)
    # u_bk = np.ones((variables.bs_number, variables.file_number)) * variables.user_size
    # s_bk = np.array([variables.sizes]).repeat(variables.bs_number, axis=0)
    # t_u_s_bk = theta_est_bk * u_bk * s_bk
    # c_c_bk = t_u_s_bk / variables.v_bb
    # c_x_bk = (t_u_s_bk / variables.v_cb - t_u_s_bk / variables.v_bb).sum(axis=0).reshape((1, t_u_s_bk.shape[1]))
    # cvx_object_c = np.concatenate([c_c_bk, c_x_bk]).reshape(c_c_bk.size + c_x_bk.size)
    # cvx_st_g = \
    #     np.zeros(shape=(cvx_object_c.size, variables.bs_number + variables.file_number * 2 + cvx_object_c.size * 2))
    # cvx_st_h = np.zeros(variables.bs_number + variables.file_number * 2 + cvx_object_c.size * 2)
    # _offset = 0
    # for bs in xrange(variables.bs_number):
    #     row = xrange(bs * variables.file_number, bs * variables.file_number + variables.file_number)
    #     column = bs + _offset
    #     cvx_st_g[row, column] = -1 * s_k
    #     cvx_st_h[column] = variables.bs_memory - s_k.sum()
    # _offset += variables.bs_number
    # for k in xrange(variables.file_number):
    #     row = xrange(k, k + cvx_object_c.size, variables.file_number)
    #     column = k + _offset
    #     cvx_st_g[row, column] = [1] * (len(row) - 1) + [-1]
    #     cvx_st_h[column] = variables.bs_number - 1
    # _offset += variables.file_number
    # for k in xrange(variables.file_number):
    #     row = xrange(k, k + cvx_object_c.size, variables.file_number)
    #     column = k + _offset
    #     cvx_st_g[row, column] = [-1] * (len(row) - 1) + [variables.bs_number]
    #     cvx_st_h[column] = 0
    # _offset += variables.file_number
    # cvx_st_g[:, _offset: _offset + cvx_object_c.size] = np.identity(cvx_object_c.size)
    # cvx_st_h[_offset: _offset + cvx_object_c.size] = 1
    # _offset += cvx_object_c.size
    # cvx_st_g[:, _offset:] = -1 * np.identity(cvx_object_c.size)
    # cvx_st_h[_offset:] = 0
    # c, g, h = matrix(cvx_object_c), matrix(cvx_st_g.T), matrix(cvx_st_h)
    # solution = solvers.lp(c, g, h)
    # return solution
