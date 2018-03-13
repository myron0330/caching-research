# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from __future__ import division
import heapq
import pickle
import numpy as np
from core.basic import BaseStation
from utils.dict_utils import DefaultDict
from utils.random_utils import zipf_array
from . algorithms import branch_and_bound, recover_from_
from . variables import Variables
from . tools import calculate_rewards


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
        self.q_value = 0
        self.q_values = list()
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

    def iter_with_q_learning_(self, algorithm, circles=300, dump=True, prefix=''):
        """
        algorithm iteration

        Args:
            algorithm(func): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
            prefix(string): prefix
        """
        while self.t < circles:
            if self.t == 0:
                theta_est_bk = self.theta_est_bk
            else:
                self.theta_est_bk += self.d_bkt[self.t-1]
                theta_est_bk = self.theta_est_bk / (self.variables.user_size * self.t)
                theta_est_bk *= (1 + self.variables.beta * self.c_bkt[self.t-1])
            self._caching_files(algorithm, theta_est_bk=theta_est_bk, initialize_circles=0)
            self._observe_demands()
            self._calculate_rewards()
            # self._calculate_q_value()
            self.t += 1
        if dump:
            performance_file = \
                '../performance/{}.rewards.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                        algorithm.func_name,
                                                                        self.variables.bs_number,
                                                                        self.variables.file_number,
                                                                        self.variables.bs_memory,
                                                                        self.variables.user_size,
                                                                        self.variables.zipf_a)
            pickle.dump(self.rewards, open(performance_file, 'w+'))

            c_bkt_file = \
                '../performance/{}.c_bkt.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                      algorithm.func_name,
                                                                      self.variables.bs_number,
                                                                      self.variables.file_number,
                                                                      self.variables.bs_memory,
                                                                      self.variables.user_size,
                                                                      self.variables.zipf_a)
            pickle.dump(self.c_bkt, open(c_bkt_file, 'w+'))
            d_bkt_file = \
                '../performance/{}.d_bkt.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                      algorithm.func_name,
                                                                      self.variables.bs_number,
                                                                      self.variables.file_number,
                                                                      self.variables.bs_memory,
                                                                      self.variables.user_size,
                                                                      self.variables.zipf_a)
            pickle.dump(self.d_bkt, open(d_bkt_file, 'w+'))
            # q_value_file = \
            #     '../performance/{}.Q-value.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
            #                                                             algorithm.func_name,
            #                                                             self.variables.bs_number,
            #                                                             self.variables.file_number,
            #                                                             self.variables.bs_memory,
            #                                                             self.variables.user_size,
            #                                                             self.variables.zipf_a)
            # pickle.dump(self.q_values, open(q_value_file, 'w+'))
        return self.rewards

    def _calculate_q_value(self):
        """
        Calculate q value.
        """
        self.q_value = (1 - self.variables.alpha) * self.q_value + self.variables.alpha * sum(self.rewards[-1].values())
        self.q_values.append(self.q_value)

    def iter_with_(self, algorithm, circles=300, dump=True, prefix=''):
        """
        algorithm iteration

        Args:
            algorithm(func): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
            prefix(string): prefix
        """
        while self.t < circles:
            if self.t == 0:
                theta_multiplier = 1
            else:
                theta_multiplier = 1 + self.variables.beta * self.c_bkt[self.t-1]
            self._caching_files(algorithm, theta_multiplier=theta_multiplier)
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1
        if dump:
            performance_file = \
                '../performance/{}.rewards.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                        algorithm.func_name,
                                                                        self.variables.bs_number,
                                                                        self.variables.file_number,
                                                                        self.variables.bs_memory,
                                                                        self.variables.user_size,
                                                                        self.variables.zipf_a)
            pickle.dump(self.rewards, open(performance_file, 'w+'))
            c_bkt_file = \
                '../performance/{}.c_bkt.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                      algorithm.func_name,
                                                                      self.variables.bs_number,
                                                                      self.variables.file_number,
                                                                      self.variables.bs_memory,
                                                                      self.variables.user_size,
                                                                      self.variables.zipf_a)
            pickle.dump(self.c_bkt, open(c_bkt_file, 'w+'))
            d_bkt_file = \
                '../performance/{}.d_bkt.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                      algorithm.func_name,
                                                                      self.variables.bs_number,
                                                                      self.variables.file_number,
                                                                      self.variables.bs_memory,
                                                                      self.variables.user_size,
                                                                      self.variables.zipf_a)
            pickle.dump(self.d_bkt, open(d_bkt_file, 'w+'))
        return self.rewards

    def find_optimal_with_bnd_(self, comparison_algorithm, circles=300, dump=True, fixed_theta=False,
                               prefix=''):
        """
        algorithm iteration

        Args:
            comparison_algorithm(func): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
            fixed_theta(boolean): whether to user fixed theta
            prefix(string): prefix
        """
        theta_est_bkt = dict()
        zipf_func = \
            (lambda x, n: x ** (-self.variables.zipf_a) / sum([(_ + 1) ** (-self.variables.zipf_a) for _ in xrange(n)]))
        theta_est_bk = np.array([[zipf_func(_ + 1, self.variables.file_number)
                                  for _ in xrange(self.variables.file_number)]] * self.variables.bs_number)
        while self.t < circles:
            self._caching_files(comparison_algorithm)
            theta_est_bkt[self.t] = self.theta_est_bk if not fixed_theta else theta_est_bk
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1
        self.t = 0
        rewards = list()
        while self.t < circles:
            c_bkt = branch_and_bound(self.variables, theta_est_bkt[self.t], self.d_bkt[self.t])
            reward = calculate_rewards(self.variables, c_bkt, self.d_bkt[self.t])
            if sum(self.rewards[self.t].values()) > sum(reward.values()):
                rewards.append(self.rewards[self.t])
            else:
                rewards.append(reward)
            self.t += 1
        if dump:
            style = 'fixed' if fixed_theta else 'dynamic'
            performance_file = \
                '../performance/{}.rewards.{}.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                           branch_and_bound.func_name,
                                                                           style,
                                                                           self.variables.bs_number,
                                                                           self.variables.file_number,
                                                                           self.variables.bs_memory,
                                                                           self.variables.user_size,
                                                                           self.variables.zipf_a)
            pickle.dump(rewards, open(performance_file, 'w+'))
        return rewards

    def iter_with_greedy_(self, comparison_algorithm, circles=300, dump=True, prefix=''):
        """
        algorithm iteration

        Args:
            comparison_algorithm(func): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
            prefix(string): prefix
        """
        theta_est_bkt = dict()
        while self.t < circles:
            self._caching_files(comparison_algorithm)
            theta_est_bkt[self.t] = self.theta_est_bk
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1

        self.t = 0
        rewards = list()
        while self.t < circles:
            c_bkt = recover_from_(self.variables, theta_est_bkt[self.t])
            reward = calculate_rewards(self.variables, c_bkt, self.d_bkt[self.t])
            if sum(self.rewards[self.t].values()) > sum(reward.values()):
                rewards.append(self.rewards[self.t])
            else:
                rewards.append(reward)
            self.t += 1
        if dump:
            performance_file = \
                '../performance/{}.rewards.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                        branch_and_bound.func_name,
                                                                        self.variables.bs_number,
                                                                        self.variables.file_number,
                                                                        self.variables.bs_memory,
                                                                        self.variables.user_size,
                                                                        self.variables.zipf_a)
            pickle.dump(rewards, open(performance_file, 'w+'))
        return rewards

    def comparison_(self, algorithm=(lambda x: x), circles=300, dump=True, prefix=''):
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
            print 'Iteration: {}'.format(self.t)
            crf[self.t] = func(zero) + func(self.t * one - last) * crf[self.t - 1] * self.c_bkt[self.t - 1]
            last += self.c_bkt[self.t - 1] * one * np.sign(self.d_bkt[self.t - 1])
            file_info = self.variables.file_info
            for bs in xrange(self.variables.bs_number):
                row_crf = list(crf[self.t][bs, :])
                if self.t == 0:
                    files = sorted(range(self.variables.file_number), reverse=True)
                    heap = [{'crf': value, 'key': files[_]} for _, value in enumerate(row_crf)]
                    if algorithm.func_name == 'lfu':
                        heap = heap[::-1][0::2] + heap[::-1][1::2]
                    else:
                        heap = heap[::-1][1:] + heap[::-1][:1]
                else:
                    for item in heap:
                        item['crf'] = float(row_crf[item['key']])
                    heap = heapq.nlargest(len(heap), heap, key=lambda x: x['crf'])
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
                '../performance/{}.rewards.{}.{}-{}-{}-{}-{}.pk'.format(prefix,
                                                                        algorithm.func_name,
                                                                        self.variables.bs_number,
                                                                        self.variables.file_number,
                                                                        self.variables.bs_memory,
                                                                        self.variables.user_size,
                                                                        self.variables.zipf_a)
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
        offset = 100000000
        return zipf_array(a=self.variables.zipf_a, low_bound=0,
                          up_bound=len(self.variables.files),
                          size=self.variables.users[bs_identity],
                          seed=(self.t * self.variables.bs_number + bs_identity) * self.variables.user_size+offset)

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

    def _caching_files(self, algorithm=None, initialize_circles=None, theta_est_bk=None, theta_multiplier=None):
        """
        Caching files at time slot t

        Args:
            algorithm(func): algorithm
            initialize_circles(int): initialize circles
        """
        initialize_circles = initialize_circles if initialize_circles is not None else self.variables.file_number
        if self.t < initialize_circles:
            self.c_bkt[self.t][:, self.variables.file_number - self.t - 1] = 1
        else:
            self.theta_est_bk = theta_est_bk \
                if theta_est_bk is not None else self.theta_hat_bk + np.sqrt(3 * np.log(self.t) / (2 * self.t_bk))
            if theta_multiplier is not None:
                self.theta_est_bk *= theta_multiplier
            self.c_bkt[self.t] = algorithm(self.variables, self.theta_est_bk, d_bkt=self.d_bkt[self.t])

    def _calculate_rewards(self, alpha=1.):
        """
        Calculate rewards of users
        """
        self.rewards.append(calculate_rewards(self.variables, self.c_bkt[self.t], self.d_bkt[self.t], alpha=alpha))
