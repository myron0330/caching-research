# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from . variables import *
from . core import BaseStation


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self):
        self.base_stations = map(BaseStation, base_stations)
        self.users = users
        self.files = files
        self.sizes = sizes

    def initialize(self):
        pass

global_agent = Agent()
