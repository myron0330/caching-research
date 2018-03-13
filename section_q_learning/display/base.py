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
