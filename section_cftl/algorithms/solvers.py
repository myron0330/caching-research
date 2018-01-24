# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
import numpy as np
from cvxpy import *


class SolverVariable(object):

    def __init__(self, uk_shape, uk_size, theta_uk,
                 memory, file_size_k, l_uk0, l_ukb,
                 neighbor_size_dict):
        self.uk_shape = uk_shape
        self.uk_size = uk_size
        self.theta_uk = theta_uk
        self.memory = memory
        self.file_size_k = file_size_k
        self.l_uk0 = l_uk0
        self.l_ukb = l_ukb
        self.neighbor_size_dict = neighbor_size_dict

    @classmethod
    def from_agent(cls, agent, solver='solve_x'):
        """
        Generate from agent
        Args:
            agent(obj): agent
            solver(string): solver name
        """
        parameters = {
            'uk_shape': agent.x_uk.shape,
            'uk_size': agent.x_uk.size,
            'theta_uk': agent.theta_uk,
            'memory': agent.variables.user_memory if solver == 'solve_x' else agent.variables.bs_memory,
            'file_size_k': np.array(agent.variables.file_size),
            'l_uk0': agent.l_uk0,
            'l_ukb': agent.l_ukb,
            'neighbor_size_dict': {key: len(value) for key, value in agent.neighbor_ub.iteritems()}
        }
        return cls(**parameters)


def solve_x(agent):
    """
    Solve matrix x

    Args:
        agent(obj): agent
    """

    variable = SolverVariable.from_agent(agent, solver='solve_x')
    y_k_inv = 1 - agent.y_k
    optimal_x_inv = Variable(variable.uk_size)
    y_uk_inv = np.zeros(variable.uk_shape)
    constraints = [
        optimal_x_inv >= 0,
        optimal_x_inv <= 1,
    ]
    for u in xrange(variable.uk_shape[0]):
        neighbor_size = variable.neighbor_size_dict[u]
        y_uk_inv[u, :] = y_k_inv ** neighbor_size
        user_optimal_x_inv = optimal_x_inv[u*variable.uk_shape[1]:(u+1)*variable.uk_shape[1]]
        constraints.append(
            sum_entries(variable.file_size_k.T * (1 - user_optimal_x_inv)) <= variable.memory)
    coefficient = variable.theta_uk * (variable.l_uk0 - variable.l_ukb) * y_uk_inv + variable.l_ukb
    multiplier = coefficient.reshape(variable.uk_size)
    objects = Minimize(multiplier * optimal_x_inv)
    problem = Problem(objects, constraints)
    problem.solve()
    x_inv = optimal_x_inv.value
    optimal_x = np.array((1 - x_inv).reshape(variable.uk_shape))
    return optimal_x


def solve_y(agent):
    """
    Solve array y
    Args:
        agent(obj): agent
    """
    variable = SolverVariable.from_agent(agent, solver='solve_y')
    x_uk = agent.x_uk
    optimal_y_inv = Variable(variable.uk_shape[1])
    constraints = [
        optimal_y_inv >= 0,
        optimal_y_inv <= 1,
        sum_entries(variable.file_size_k.T * (1 - optimal_y_inv)) <= variable.memory
    ]
    y_uk = list()
    for u in xrange(variable.uk_shape[0]):
        neighbor_size = variable.neighbor_size_dict[u]
        y_uk.append(power(optimal_y_inv, neighbor_size))
    y_uk = vstack(*y_uk)
    coefficient = variable.theta_uk * (variable.l_uk0 - variable.l_ukb) * x_uk
    multiplier = coefficient.reshape(variable.uk_size)
    objects = Minimize(multiplier * y_uk)
    problem = Problem(objects, constraints)
    problem.solve()
    y_inv = optimal_y_inv.value
    optimal_y = np.array((1 - y_inv)).T
    return optimal_y


__all__ = [
    'SolverVariable',
    'solve_x',
    'solve_y'
]
