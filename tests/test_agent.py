# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of agent
# **********************************************************************************#
import unittest
from caching.agent import global_agent


class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = global_agent

    def test_init(self):
        print self.agent.base_stations[0].identity
        print self.agent.sizes
