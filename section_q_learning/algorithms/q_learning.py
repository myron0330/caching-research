# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from . lp_solvers import primal_dual_recover


def global_q_learning(variables, theta_est_bk, recover=True, lp_method=None, *args, **kwargs):
    """
    Using global q learning method to solve the relaxing problem, recover with knapsack dynamic programming.

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
        lp_method(function): which lp method to use
        recover(boolean): whether to recover the algorithm
    """
    return primal_dual_recover(variables, theta_est_bk, recover=recover, lp_method=lp_method, *args, **kwargs)


def distributed_q_learning(variables, theta_est_bk, recover=True, lp_method=None, *args, **kwargs):
    """
    Using distributed q learning method to solve the relaxing problem, recover with knapsack dynamic programming.

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
        lp_method(function): which lp method to use
        recover(boolean): whether to recover the algorithm
    """
    return primal_dual_recover(variables, theta_est_bk, recover=recover, lp_method=lp_method, *args, **kwargs)
