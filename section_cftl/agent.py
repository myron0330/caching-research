# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Agent files, the player of this problem
# **********************************************************************************#
from __future__ import division
import pickle
import numpy as np
from core.basic import BaseStation
from utils.dict_utils import DefaultDict
from utils.random_utils import zipf_array
from utils.rewards_utils import calculate_cftl_rewards
from . variables import Variables
from . algorithms.solvers import *


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


def _get_user_bs_transmission_rate(variables, d_ub, bs_type='macro'):
    """
    Get user bs transmission rate
    Args:
        variables(obj): global variable
        d_ub(matrix): user bs distance info dict
        bs_type(string): bs type

    Returns:
        matrix: r_ub
    """
    if bs_type == 'macro':
        return variables.r_u0 * np.ones(d_ub.shape)
    beta = variables.beta_0u if bs_type == 'macro' else variables.beta_bu
    p = variables.p_0 if bs_type == 'macro' else variables.p_b
    g_ub = beta * (d_ub**(-variables.alpha)) * p
    gamma_ub = p * g_ub / (variables.sigma ** 2)
    r_ub = variables.w * np.log2(1 + gamma_ub)
    return r_ub


def _get_users_latency(variables, r_ub, neighbor_ub=None):
    """
    Get users latency
    Args:
        variables(obj): global variable
        r_ub(matrix): transmission rate matrix among u, b
        neighbor_ub(dict): neighbor information

    Returns:
        matrix: l_uk
    """
    neighbor_ub = neighbor_ub if neighbor_ub is not None else {_: [0] for _ in variables.users}
    file_size = variables.file_size
    l_uk = np.zeros((variables.user_number, variables.file_number))
    for u in xrange(l_uk.shape[0]):
        neighbor_bs = neighbor_ub[u]
        if neighbor_bs:
            u_transmission_rates = r_ub[u, neighbor_bs]
        else:
            u_transmission_rates = variables.r_u0
        for k in xrange(l_uk.shape[1]):
            size = file_size[k]
            latency = np.mean(size / u_transmission_rates)
            l_uk[u, k] = float(latency)
    return l_uk


class Agent(object):
    """
    The global player, whom to solve the caching problem.
    """
    def __init__(self, variables):
        self.t = 0
        self.variables = variables
        self.theta_uk = np.zeros((self.variables.user_number, self.variables.file_number))
        self.x_uk = np.zeros((self.variables.user_number, self.variables.file_number))
        self.y_k = np.zeros((1, self.variables.file_number))
        self.macro_bs_network = pickle.load(open(self.variables.macro_bs_network, 'r+'))
        self.bs_network = pickle.load(open(self.variables.bs_network, 'r+'))
        self.users_network = pickle.load(open(self.variables.users_network, 'r+'))
        self.d_ub = _get_users_bs_distance(bs_network=self.bs_network,
                                           users_network=self.users_network,
                                           distance_scale=self.variables.distance_scale)
        self.d_u0 = _get_users_bs_distance(bs_network=self.macro_bs_network,
                                           users_network=self.users_network,
                                           distance_scale=self.variables.distance_scale)
        self.neighbor_ub = _get_user_neighbor_bs(self.d_ub,
                                                 radius=self.variables.radius*self.variables.distance_scale)
        self.r_ub = _get_user_bs_transmission_rate(self.variables, self.d_ub, bs_type='sub')
        self.r_u0 = _get_user_bs_transmission_rate(self.variables, self.d_u0, bs_type='macro')
        self.l_ukb = _get_users_latency(self.variables, self.r_ub, self.neighbor_ub)
        self.l_uk0 = _get_users_latency(self.variables, self.r_u0)
        self.l_uk_diff = self.l_uk0 - self.l_ukb
        self.rewards = list()
        self._build()

    def _build(self):
        """
        Build agent.
        """
        self._estimate_theta()

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

    def _estimate_theta(self, theta_est=None):
        """
        Theta estimation

        Args:
            theta_est(array): theta est
        """
        if theta_est is None:
            zipf_func = \
                (lambda x, n: x ** (-self.variables.zipf_a) / sum([(_ + 1) ** (-self.variables.zipf_a)
                                                                   for _ in xrange(n)]))
            theta_est = np.array([zipf_func(_ + 1, self.variables.file_number)
                                  for _ in xrange(self.variables.file_number)])
        for _ in xrange(self.theta_uk.shape[0]):
            self.theta_uk[_, :] = theta_est

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
        raise NotImplementedError

    def _solving_by(self, algorithm=None):
        """
        solving problems algorithms
        """
        raise NotImplementedError
