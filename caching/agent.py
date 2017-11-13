# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from __future__ import division
import heapq
import pickle
import numpy as np
from . basic import BaseStation
from . basic.tools import calculate_rewards
from . variables import Variables
from . utils.random_utils import zipf_array
from . utils.dict_utils import DefaultDict
from . algorithms import branch_and_bound, primal_dual_recover


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

    def iter_with_(self, algorithm, circles=300, dump=True):
        """
        algorithm iteration

        Args:
            algorithm(function): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
        """
        while self.t < circles:
            self._caching_files(algorithm)
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1
        if dump:
            performance_file = \
                '../performance/rewards.{}.{}-{}-{}-{}.pk'.format(algorithm.func_name,
                                                                  self.variables.bs_number,
                                                                  self.variables.file_number,
                                                                  self.variables.bs_memory,
                                                                  self.variables.user_size)
            pickle.dump(self.rewards, open(performance_file, 'w+'))
        return self.rewards

    def find_optimal_with_bnd_(self, comparison_algorithm, circles=300, dump=True):
        """
        algorithm iteration

        Args:
            comparison_algorithm(function): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
        """
        theta_est = dict()
        while self.t < circles:
            self._caching_files(comparison_algorithm)
            theta_est[self.t] = self.theta_est_bk
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1
        self.t = 0
        rewards = list()
        while self.t < circles:
            c_bkt = branch_and_bound(self.variables, theta_est[self.t], self.d_bkt[self.t])
            rewards.append(calculate_rewards(self.variables, c_bkt, self.d_bkt[self.t]))
            self.t += 1
        if dump:
            performance_file = \
                '../performance/rewards.{}.{}-{}-{}-{}.pk'.format(branch_and_bound.func_name,
                                                                  self.variables.bs_number,
                                                                  self.variables.file_number,
                                                                  self.variables.bs_memory,
                                                                  self.variables.user_size)
            pickle.dump(rewards, open(performance_file, 'w+'))
        return rewards

    def comparison_(self, algorithm=(lambda x: x), circles=300, dump=True):
        """
        Reference algorithm iterator.
        """
        func = np.vectorize(algorithm)
        crf = DefaultDict(np.zeros((self.variables.bs_number, self.variables.file_number)))
        last = np.zeros((self.variables.bs_number, self.variables.file_number))
        zero = np.zeros((self.variables.bs_number, self.variables.file_number))
        one = np.ones((self.variables.bs_number, self.variables.file_number))
        tail = dict()
        while self.t < circles:
            crf[self.t] = func(zero) + func(self.t * one - last) * crf[self.t - 1] * self.c_bkt[self.t - 1]
            last += self.c_bkt[self.t - 1] * one
            file_info = self.variables.file_info
            for bs in xrange(self.variables.bs_number):
                row_crf = list(crf[self.t][bs, :])
                files = sorted(range(self.variables.file_number), reverse=True)
                heap = [{'crf': value, 'key': files[_]} for _, value in enumerate(row_crf)]
                if self.t == 0:
                    if algorithm.func_name == 'lfu':
                        heapq.heapify(heap)
                    else:
                        heap = heapq.nsmallest(len(heap), heap, key=lambda x: x['crf'])
                        heap = heap[0::2] + heap[1::2]
                else:
                    heapq.heapify(heap)
                sizes = 0
                for _, d in enumerate(heap):
                    f = d['key']
                    if sizes + file_info[f] < self.variables.bs_memory:
                        if tail.get(bs) is not None and tail.get(bs) == f:
                            continue
                        sizes += file_info[f]
                        self.c_bkt[self.t][bs, f] = 1
                    else:
                        tail[bs] = f
                        break
            self._observe_demands()
            self._calculate_rewards()
            self.t += 1
        if dump:
            performance_file = \
                '../performance/rewards.{}.{}-{}-{}-{}.pk'.format('lfu',
                                                                  self.variables.bs_number,
                                                                  self.variables.file_number,
                                                                  self.variables.bs_memory,
                                                                  self.variables.user_size)
            pickle.dump(self.rewards, open(performance_file, 'w+'))
        return self.rewards

    # def lru_(self, circles=300, dump=True):
    #     """
    #     Reference algorithm iterator.
    #     """
    #     lru = np.vectorize(lambda x: (1./2)**x)
    #     crf = DefaultDict(np.zeros((self.variables.bs_number, self.variables.file_number)))
    #     while self.t < circles:
    #         self.c_bkt[self.t] =

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
                          seed=(self.t * self.variables.bs_number + bs_identity) * self.variables.user_size+100000)

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

    def _caching_files(self, algorithm=None, initialize_circles=None):
        """
        Caching files at time slot t

        Args:
            algorithm(function): algorithm
            initialize_circles(int): initialize circles
        """
        initialize_circles = initialize_circles if initialize_circles is not None else self.variables.file_number
        if self.t < initialize_circles:
            self.c_bkt[self.t][:, self.variables.file_number - self.t - 1] = 1
        else:
            self.theta_est_bk = self.theta_hat_bk + np.sqrt(3 * np.log(self.t) / (2 * self.t_bk))
            self.c_bkt[self.t] = algorithm(self.variables, self.theta_est_bk, d_bkt=self.d_bkt[self.t])

    def _calculate_rewards(self):
        """
        Calculate rewards of users
        """
        self.rewards.append(calculate_rewards(self.variables, self.c_bkt[self.t], self.d_bkt[self.t]))
