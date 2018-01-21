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
from utils.rewards_utils import calculate_cftl_rewards
from . variables import Variables


def _calculate_distance(position_a, position_b, distance_scale=1.):
    """
    Calculate distance.
    """
    return distance_scale * sum((position_a - position_b)**2)**0.5


def _get_users_bs_distance(bs_network, users_network, distance_scale=1.):
    """
    Calculate users - base stations distances among bs and users.

    Returns:
        matrix: R**(users_number, bs_number)
    """
    bs_layout = bs_network.layout
    users_layout = users_network.layout
    user_bs_distance = np.zeros((users_network.node_number, bs_network.node_number))
    for user, user_position in users_layout.iteritems():
        for bs, bs_position in bs_layout.iteritems():
            user_bs_distance[user, bs] = _calculate_distance(user_position, bs_position,
                                                             distance_scale=distance_scale)
    return user_bs_distance


def _get_user_neighbor_bs(user_bs_distance, radius):
    """

    Args:
        user_bs_distance(matrix): user bs distance info dict
        radius(float): radius information

    Returns:
        dict: key-value: user_node --> bs neighbors list
    """
    user_neighbor_bs = dict()
    for user in xrange(user_bs_distance.shape[0]):
        distance = user_bs_distance[user, :]
        neighbors = list(np.where(distance < radius)[0])
        user_neighbor_bs[user] = neighbors
    return user_neighbor_bs


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self, variables):
        self.t = 0
        self.variables = variables
        self.theta_est_uk = np.zeros((self.variables.user_number, self.variables.file_number))
        self.x_uk = np.zeros((self.variables.user_number, self.variables.file_number))
        self.y_k = np.zeros((1, self.variables.file_number))
        self.bs_network = pickle.load(open(self.variables.bs_network, 'r+'))
        self.users_network = pickle.load(open(self.variables.users_network, 'r+'))
        self.user_bs_distance = _get_users_bs_distance(bs_network=self.bs_network,
                                                       users_network=self.users_network,
                                                       distance_scale=self.variables.distance_scale)
        self.user_neighbor_bs = _get_user_neighbor_bs(self.user_bs_distance,
                                                      radius=self.variables.radius*self.variables.distance_scale)
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
            self._caching_files(algorithm)
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

    def find_optimal_with_bnd_(self, comparison_algorithm, circles=300, dump=True, fixed_theta=False,
                               prefix=''):
        """
        algorithm iteration

        Args:
            comparison_algorithm(function): algorithm
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
            theta_est_bkt[self.t] = self.theta_est_uk if not fixed_theta else theta_est_bk
            self._observe_demands()
            self._calculate_rewards()
            self.t += 1
        self.t = 0
        rewards = list()
        while self.t < circles:
            c_bkt = branch_and_bound(self.variables, theta_est_bkt[self.t], self.y_k[self.t])
            reward = calculate_mab_rewards(self.variables, c_bkt, self.y_k[self.t])
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
            comparison_algorithm(function): algorithm
            circles(int): max iteration circles
            dump(boolean): whether to dump results
            prefix(string): prefix
        """
        theta_est_bkt = dict()
        while self.t < circles:
            self._caching_files(comparison_algorithm)
            theta_est_bkt[self.t] = self.theta_est_uk
            self._observe_demands()
            self._mab_update()
            self._calculate_rewards()
            self.t += 1

        self.t = 0
        rewards = list()
        while self.t < circles:
            c_bkt = recover_from_(self.variables, theta_est_bkt[self.t])
            reward = calculate_mab_rewards(self.variables, c_bkt, self.y_k[self.t])
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
            crf[self.t] = func(zero) + func(self.t * one - last) * crf[self.t - 1] * self.x_uk[self.t - 1]
            last += self.x_uk[self.t - 1] * one * np.sign(self.y_k[self.t - 1])
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
                        self.x_uk[self.t][bs, f] = 1
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
        # 1000000
        # 100000000
        return zipf_array(a=self.variables.zipf_a, low_bound=0,
                          up_bound=len(self.variables.files),
                          size=self.variables.users[bs_identity],
                          seed=(self.t * self.variables.bs_number + bs_identity) * self.variables.user_size+1000000)

    def _observe_demands(self):
        """
        Observe demands at time slot t
        """
        for base_station in self.variables.base_stations:
            identity = base_station.identity
            demand_array = self._generate_demands(identity)
            base_station.observe_(demands=demand_array)
            demand_statics = [base_station.demand_statics[_] for _ in xrange(self.variables.file_number)]
            self.y_k[self.t][identity, :] = demand_statics

    def _caching_files(self, algorithm=None, initialize_circles=None):
        """
        Caching files at time slot t

        Args:
            algorithm(function): algorithm
            initialize_circles(int): initialize circles
        """
        raise NotImplementedError

    def _calculate_rewards(self, alpha=1.):
        """
        Calculate rewards of users
        """
        self.rewards.append(calculate_cftl_rewards(self.variables, self.x_uk[self.t], self.y_k[self.t], alpha=alpha))

