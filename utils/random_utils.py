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


# def zipf_array(a, low_bound=None, up_bound=None, size=None, seed=100000):
#     """
#     Get random variables that satisfies Zipf law.
#
#     Args:
#         a(float): parameter of zipf law, > 1
#         low_bound(int): lowest bound
#         up_bound(int): highest bound
#         size(int): size of array
#         seed(int): the seed of random
#     """
#     size = size if size is not None else DEFAULT_SIZE
#     counter, array = -1, list()
#     while len(array) < size:
#         counter += 1
#         candidate = int(zipf.rvs(a, size=1, random_state=counter+seed))
#         if low_bound and candidate < low_bound:
#             continue
#         if up_bound and candidate > up_bound:
#             continue
#         array.append(candidate)
#     return array


def zipf_probabilities(a, low_bound=None, up_bound=None):
    """
    Zipf probabilities
    """
    candidates = range(low_bound+1, up_bound+1)
    aggregation = sum([_ ** (-a) for _ in candidates])
    probabilities = list()
    for _ in candidates:
        probabilities.append(_ ** (-a) / aggregation)
    return probabilities


def probability_random(values, probabilities, seed=0):
    """
    Generate probability random number
    """
    random.seed(seed)
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(values, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    item = locals().get('item')
    return item


def zipf_array(a, low_bound=None, up_bound=None, size=None, seed=100000):
    """
    Get random variables that satisfies Zipf law.

    Args:
        a(float): parameter of zipf law
        low_bound(int): lowest bound
        up_bound(int): highest bound
        size(int): size of array
        seed(int): the seed of random
    """
    values = range(low_bound+1, up_bound+1)
    probabilities = zipf_probabilities(a, low_bound=low_bound, up_bound=up_bound)
    size = size if size is not None else DEFAULT_SIZE
    counter, array = -1, list()
    while len(array) < size:
        counter += 1
        candidate = probability_random(values, probabilities, seed=(counter + seed))
        array.append(candidate)
    return array


def random_state(rate_array, seed=0):
    """
    Generate random state base on rate array.

    Args:
        rate_array(array like): rate array, sumation is integer and greater than 1.
        seed(int): random seed
    """
    threshold, output = 0, 0
    random.seed(seed)
    rand_number = random.randint(1, sum(rate_array))
    for index, item in enumerate(rate_array):
        threshold += item
        if rand_number <= threshold:
            break
        output += 1
    return output


def random_choose_(percent=0.05, lower_bound=0, upper_bound=100, matrix_size=2000, seed=0):
    """
    Random choose.
    Args:
        percent:
        lower_bound:
        upper_bound:
        matrix_size:
        seed:
    Returns:

    """
    result = set()
    while len(result) < int(percent * matrix_size):
        random.seed(seed)
        result.add(random.randint(lower_bound, upper_bound))
        seed += 1
    return result
