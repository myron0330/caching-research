# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from __future__ import division
import pickle
import numpy as np
from . core import BaseStation
from . variables import Variables
from . utils.random_utils import zipf_array
from . utils.dict_utils import DefaultDict


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self, variables):
        # initialize parameters
        self.variables = variables
        # intermediate variables
        self.t = 0
        self.theta_hat_bk = np.zeros((self.variables.bs_number, self.variables.file_number))
        self.theta_est_bk = np.zeros((self.variables.bs_number, self.variables.file_number))
        self.t_bk = np.zeros((self.variables.bs_number, self.variables.file_number))
        self.c_bkt = DefaultDict(np.zeros((self.variables.bs_number, self.variables.file_number)))
        self.d_bkt = DefaultDict(np.zeros((self.variables.bs_number, self.variables.file_number)))
        self.rewards = list()

    @classmethod
    def from_(cls, cfg_file=None):
        """
        Init from cfg file

        Args:
            cfg_file(string): config file name
        """
        variables = Variables.from_(cfg_file=cfg_file)
        variables.base_stations = map(lambda x: BaseStation(x, memory=variables.bs_memory), variables.base_stations)
        return cls(variables)

    def iter_with_(self, algorithm, circles=300):
        """
        algorithm iteration

        Args:
            algorithm(function): algorithm
            circles(int): max iteration circles
        """
        while self.t < circles:
            self._caching_files(algorithm)
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            print '*' * 60
            print 'current time', self.t
            # print self.c_bkt[self.t]
            # print self.theta_hat_bk
            # print self.t_bk
            # print self.theta_est_bk
            # print self.theta_hat_bk
            print self.rewards[self.t]
            print '*' * 60
            print '\n'
            self.t += 1
        pickle.dump(self.rewards, open('../performance/rewards.pk', 'w+'))

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
                          seed=(self.t * self.variables.bs_number + bs_identity) * self.variables.user_size)

    def _observe_demands(self):
        """
        Observe demands at time slot t
        """
        for base_station in self.variables.base_stations:
            identity = base_station.identity
            demand_array = self._generate_demands(identity)
            base_station.observe_(demands=demand_array)
            demand_statics = [base_station.demand_statics[_] for _ in xrange(self.variables.file_number)]
            self.d_bkt[self.t][identity, :] = demand_statics

    def _mab_update(self):
        """
        Update parameters
        """
        if self.t < self.variables.file_number:
            self.theta_hat_bk += self.d_bkt[self.t] * self.c_bkt[self.t] / self.variables.user_size
        else:
            self.theta_hat_bk = \
                (self.theta_hat_bk * self.t_bk +
                 self.d_bkt[self.t] * self.c_bkt[self.t] / self.variables.user_size) / (self.t_bk + self.c_bkt[self.t])
        self.t_bk += self.c_bkt[self.t]

    def _caching_files(self, algorithm=None):
        """
        Caching files at time slot t

        Args:
            algorithm(function): algorithm
        """
        if self.t < self.variables.file_number:
            self.c_bkt[self.t][:, self.t] = 1
        else:
            self.theta_est_bk = self.theta_hat_bk + np.sqrt(3 * np.log(self.t) / (2 * self.t_bk))
            self.c_bkt[self.t] = algorithm(self.variables, self.theta_est_bk)

    def _calculate_rewards(self):
        """
        Calculate rewards of users
        """
        delta = max(self.variables.sizes) * (1 / self.variables.v_bd + 1 / self.variables.v_cb)
        c_bkt = self.c_bkt[self.t]
        d_bkt = self.d_bkt[self.t]
        c_kt = self.c_bkt[self.t].sum(axis=0)
        v_bd, v_bb, v_cb = self.variables.v_bd, self.variables.v_bb, self.variables.v_cb
        file_info = self.variables.file_info
        r_0 = 1
        rewards = dict()
        for base_station in self.variables.base_stations:
            identity = base_station.identity
            c_bt = c_bkt[identity, :]
            d_bt = d_bkt[identity, :]
            reward = 0
            for f in self.variables.files:
                latency = file_info[f] * (1. / v_bd + (1. - c_bt[f]) * (1. * c_kt[f] / v_bb + (1. - c_kt[f]) / v_cb))
                reward += d_bt[f] * (delta - latency) * r_0
            rewards[identity] = reward
        self.rewards.append(rewards)
