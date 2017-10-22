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
    def __init__(self, base_stations, users, files, sizes):
        self.base_stations = map(BaseStation, base_stations)
        self.users = users
        self.files = files
        self.sizes = sizes

