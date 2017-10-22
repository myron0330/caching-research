# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of utils
# **********************************************************************************#
import unittest
from caching.utils.random_utils import zipf_array


class TestRandomUtils(unittest.TestCase):

    def setUp(self):
        self.a = 2
        self.low_bound = 10
        self.high_bound = 20
        self.size = 100
        self.seed = 0

    def test_zipf_array(self):
        result = zipf_array(self.a,
                            low_bound=self.low_bound,
                            up_bound=self.high_bound,
                            size=self.size, seed=self.seed)
        print len(result), result
