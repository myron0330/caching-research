# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of agent
# **********************************************************************************#
import unittest
from caching.agent import Agent
from caching.algorithms.core import primal_dual_recover
from caching.algorithms.bnb import branch_and_bound


class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent.from_()

    def test_init(self):
        print self.agent.base_stations[0].identity
        print self.agent.base_stations[0].memory
        print self.agent.sizes
        print self.agent.theta_hat_bk

    def test_iter_with(self):
        self.agent.iter_with_(algorithm=None, circles=100)
        # print self.agent.theta_hat_bk
        # print self.agent.t_bk
        # print self.agent.c_bkt

    def test_iter_with_primal_dual_recover(self):
        self.agent.iter_with_(algorithm=primal_dual_recover, circles=500)
        # print self.agent.theta_hat_bk
        # print self.agent.t_bk
        # print self.agent.c_bkt

    def test_iter_with_branch_and_bound(self):
        self.agent.iter_with_(algorithm=branch_and_bound, circles=500)
        # print self.agent.theta_hat_bk
        # print self.agent.t_bk
        # print self.agent.c_bkt
