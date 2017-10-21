import random


DEFAULT_SIZE = 1


def randint_array(low_bound, high_bound, size=None, seed=0):
    """
    Get randint array

    Args:
        low_bound(int): lowest bound
        high_bound(int): highest bound
        size(int): size of array
        seed(int): the seed of random
    """
    size = size if size is not None else DEFAULT_SIZE
    array = list()
    for index in xrange(size):
        random.seed(index + seed)
        array.append(random.randint(low_bound, high_bound))
    return array
