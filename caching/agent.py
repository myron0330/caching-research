# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
import numpy as np
from . variables import *
from . core import BaseStation


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self):
        # initialize parameters
        self.base_stations = map(lambda x: BaseStation(x, memory=bs_memory), base_stations)
        self.users = users
        self.files = files
        self.sizes = sizes

        # intermediate variables
        self.t = 0
        self.theta_hat = np.zeros((bs_number, file_number))

    def initialize(self):
        while self.t < file_number:
            self.t += 1

global_agent = Agent()
