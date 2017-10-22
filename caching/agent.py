# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from __future__ import division
import numpy as np
from . core import BaseStation
from . variables import Variables
from . utils.random_utils import zipf_array


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self, variables):
        # initialize parameters
        self.variables = variables

        # intermediate variables
        self.time_slot = 0
        self.theta_hat_bk = np.zeros((self.variables.bs_number, self.variables.file_number))
        self.t_bk = np.zeros((self.variables.bs_number, self.variables.file_number))

    @classmethod
    def from_(cls, cfg_file=None):
        """
        Init from cfg file

        Args:
            cfg_file(string): config file name
        """
        variables = Variables.from_(cfg_file=cfg_file)
        variables.base_stations = map(BaseStation, variables.base_stations)
        return cls(variables)

    def initialize(self):
        """
        Algorithm initialize
        """
        while self.time_slot < self.variables.file_number:
            for base_station in self.variables.base_stations:
                base_station.caching_(files={self.time_slot})
                demand_array = self._generate_demands(base_station.identity)
                base_station.observe_(demands=demand_array)
                index, column = base_station.identity, self.time_slot
                self.theta_hat_bk[index, column] = base_station.demand_statics[column] / self.variables.user_size
                self.t_bk[index, column] = 1
            self.time_slot += 1

    def _generate_demands(self, bs_identity):
        """
        Generate demands based on bs identity and time slot.
        Args:
            bs_identity(int): bs identity

        Returns:
            np.array: demands of users in base station bs_identity at time t
        """
        return zipf_array(a=self.variables.zipf_a, low_bound=0,
                          up_bound=len(self.variables.files),
                          size=self.variables.users[bs_identity],
                          seed=(self.time_slot * self.variables.bs_number + bs_identity) * self.variables.user_size)
