# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of agent
# **********************************************************************************#
import unittest
from section_cmab.agent import Agent
from section_cmab.algorithms.lp_solvers import primal_dual_recover
from section_cmab.algorithms.bnb_solvers import branch_and_bound


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
