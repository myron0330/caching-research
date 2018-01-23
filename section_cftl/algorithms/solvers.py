# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
import numpy as np
from cvxpy import *


def solve_x(agent):
    """
    Solve x result
    Args:
        agent(obj): agent
    """
    uk_shape = agent.x_uk.shape
    uk_size = agent.x_uk.size
    theta_uk = agent.theta_uk
    memory = agent.variables.user_memory
    file_size_k = np.array(agent.variables.file_size)
    l_uk0 = agent.l_uk0
    l_ukb = agent.l_ukb
    y_k_inv = 1 - agent.y_k
    optimal_x_inv = Variable(uk_size)
    y_uk_inv = np.zeros(uk_shape)
    constraints = [
        optimal_x_inv >= 0,
        optimal_x_inv <= 1,
    ]
    for _ in xrange(uk_shape[0]):
        neighbor_size = len(agent.neighbor_ub[_])
        y_uk_inv[_, :] = y_k_inv ** neighbor_size
        user_optimal_x_inv = optimal_x_inv[_*uk_shape[1]:(_+1)*uk_shape[1]]
        constraints.append(sum_entries((1 - user_optimal_x_inv).T * file_size_k) <= memory)
    coefficient = theta_uk * (l_uk0 - l_ukb) * y_uk_inv + l_ukb
    multiplier = coefficient.reshape(uk_size)
    objects = Minimize(multiplier * optimal_x_inv)
    problem = Problem(objects, constraints)
    problem.solve(solver=SCS)
    x_inv = optimal_x_inv.value
    optimal_x = np.array((1 - x_inv).reshape(agent.x_uk.shape))
    return optimal_x


__all__ = [
    'solve_x'
]
