# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test cases of agent
# **********************************************************************************#
import unittest
from caching.agent import Agent
from caching.variables import *


class TestAgent(unittest.TestCase):

    def setUp(self):
        self.base_stations = base_stations
        self.users = users
        self.files = files
        self.sizes = sizes
        self.agent = Agent(self.base_stations, self.users, self.files, self.sizes)

    def test_init(self):
        print self.agent.base_stations[0].identity
        print self.agent.sizes
