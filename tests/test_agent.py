# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of agent
# **********************************************************************************#
import unittest
from caching.agent import Agent


class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent.from_()

    def test_init(self):
        print self.agent.base_stations[0].identity
        print self.agent.base_stations[0].memory
        print self.agent.sizes
        print self.agent.theta_hat_bk

    def test_initialize(self):
        self.agent.initialize()
