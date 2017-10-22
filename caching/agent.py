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
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            self = super(Agent, cls).__new__(cls)
            self.base_stations = map(BaseStation, base_stations)
            self.users = users
            self.files = files
            self.sizes = sizes
            cls._instance = self
        return cls._instance


global_agent = Agent()
