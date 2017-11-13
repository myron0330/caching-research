import random
from scipy.stats import zipf


DEFAULT_SIZE = 1


def randint_array(low_bound, up_bound, size=None, seed=0):
    """
    Get randint array

    Args:
        low_bound(int): lowest bound
        up_bound(int): highest bound
        size(int): size of array
        seed(int): the seed of random
    """
    size = size if size is not None else DEFAULT_SIZE
    array = list()
    for index in xrange(size):
        random.seed(index+seed)
        array.append(random.randint(low_bound, up_bound))
    return array


def zipf_array(a, low_bound=None, up_bound=None, size=None, seed=100000):
    """
    Get random variables that satisfies Zipf law.

    Args:
        a(float): parameter of zipf law, > 1
        low_bound(int): lowest bound
        up_bound(int): highest bound
        size(int): size of array
        seed(int): the seed of random
    """
    size = size if size is not None else DEFAULT_SIZE
    counter, array = -1, list()
    while len(array) < size:
        counter += 1
        candidate = int(zipf.rvs(a, size=1, random_state=counter+seed))
        if low_bound and candidate < low_bound:
            continue
        if up_bound and candidate > up_bound:
            continue
        array.append(candidate)
    return array
