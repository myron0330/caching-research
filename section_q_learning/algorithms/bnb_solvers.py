# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Branch and bound algorithm
# **********************************************************************************#
from __future__ import division
import numpy as np
from . lp_solvers import primal_dual_recover, primal_dual_with_candidate
from .. tools import calculate_rewards


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


class Node(object):
    """
    Tree node
    """
    def __init__(self, left=None, right=None, obj=None, height=0):
        self.left = left
        self.right = right
        self.obj = obj
        self.height = height


def traversal_add_binary_(node, height=0):
    """
    Traversal add binary variables
    Args:
        node(node): root node
        height(int): height
    """
    if node and node.left is None and node.right is None:
        node.left = Node(obj=0, height=height+1)
        node.right = Node(obj=1, height=height+1)
        return
    traversal_add_binary_(node.left, height=height+1)
    traversal_add_binary_(node.right, height=height+1)


def _get_height(node):
    """
    Get height of a tree

    Args:
        node(node): root node
    """
    if node is None:
        return 0
    return max(_get_height(node.left), _get_height(node.right)) + 1


class BinaryTree(object):
    """
    Binary tree
    """
    def __init__(self, root=None):
        self.root = root

    def generate(self, height):
        """
        Generate binary tree from height
        """
        self.root = Node()
        counter = 0
        while counter < height:
            traversal_add_binary_(self.root)
            counter += 1

    def get_height(self):
        """
        Return height of the tree
        """
        return _get_height(self.root)

    def iterator_with_(self, pruning_func=(lambda x: False), *args, **kwargs):
        """
        enumerate valid samples

        Args:
            pruning_func(function): pruning function
        """
        enumerates = list()

        def _deep_traversal(root, candidate):
            """Deep traversal"""
            if root.obj is not None:
                candidate = candidate[:root.height]
                candidate.append(root.obj)
                if pruning_func(candidate, *args, **kwargs):
                    return
                if candidate:
                    enumerates.append(candidate)
            if root.left is None or root.right is None:
                return
            _deep_traversal(root.left, candidate)
            _deep_traversal(root.right, candidate)

        _deep_traversal(self.root, list())
        return iter(enumerates)


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


if __name__ == '__main__':

    def test_pruning(candidate):
        """
        Test pruning function

        Args:
            candidate(array): array
        """
        if sum(candidate) < 6:
            return False
        return True

    tree = BinaryTree()
    tree.generate(10)
    iterator = tree.iterator_with_(pruning_func=test_pruning)
    print list(iterator)
