# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: tree utils
# **********************************************************************************#


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
