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

    def test_iter_with(self):
        self.agent.iter_with_(algorithm=None, circles=15)
        # print self.agent.theta_hat_bk
        # print self.agent.t_bk
        # print self.agent.c_bkt
