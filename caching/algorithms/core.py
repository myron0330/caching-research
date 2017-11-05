# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Core algorithms
# **********************************************************************************#
import numpy as np
from . lp_solvers import primal_dual_interior_method
from . recover import recover_from_


def primal_dual_recover(variables, theta_est_bk):
    """
    Using primal dual interior method to solve the relaxing problem, recover with knapsack dynamic programming.

    Args:
        variables(variables): variable parameters
        theta_est_bk(matrix): theta estimation
    """
    solution = np.array(primal_dual_interior_method(variables, theta_est_bk)['x'])
    c_inv_bk = solution.reshape((variables.bs_number + 1, variables.file_number))
    c_bk = (1 - c_inv_bk)[:-1, :]
    return recover_from_(variables, c_bk)
