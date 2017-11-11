# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Branch and bound algorithm
# **********************************************************************************#
from __future__ import division
import numpy as np
from . lp_solvers import primal_dual_recover, primal_dual_with_candidate
from .. basic.tools import calculate_rewards
from .. utils.tree_utils import BinaryTree


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


def _pruning_node(candidates, node):
    """
    Pruning node begin with candidate
    Args:
        candidates(list): candidate branches
        node(list): target node list
    """
    return [candidate for candidate in candidates if candidate[:len(node)] != node]


def branch_and_bound(variables, theta_est_bk, d_bkt):
    """
    Branch and bound method

    Args:
        variables(variables): variable parameters
        theta_est_bk(ndarray): theta
        d_bkt(ndarray): demands
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
            c_bkt = primal_dual_with_candidate(variables, theta_est_bk, candidate=candidate, recover=True)
            validation = _valid_solution(c_bkt)
            rewards = calculate_rewards(variables, c_bkt, d_bkt, aggregate=True)
            if rewards < incumbent[1]:
                candidates = _pruning_node(candidates, candidate)
            elif validation:
                incumbent = (c_bkt, rewards)
                candidates = _pruning_node(candidates, candidate)
        head += list(incumbent[0][_, :])
    solution = np.array(head).reshape((variables.bs_number, variables.file_number))
    return solution
