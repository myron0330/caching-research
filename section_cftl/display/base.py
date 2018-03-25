# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import numpy as np


def standardize_(array, sigma=1.5):
    """
    Standardize array

    Args:
        array(list): standardize array
        sigma(int): sigma threshold
    """
    x_mean = np.mean(array)
    x_std = np.std(array)
    return map(lambda a: max(x_mean - sigma * x_std, min(x_mean + sigma * x_std, a)), array)


def moving_average_(array, ma_periods):
    """
    moving average of array based on ma_periods.

    Args:
        array(list): array like
        ma_periods(float): ma periods
    """
    result = array[:1]
    for index in range(1, len(array)):
        start_index = max(index-ma_periods+1, 0)
        end_index = index + 1
        result.append(np.mean(array[start_index:end_index]))
    return result


if __name__ == '__main__':
    x = range(10)
    print moving_average_(x, 3)
