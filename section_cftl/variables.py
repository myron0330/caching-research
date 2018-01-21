# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: global variables
# **********************************************************************************#
import os
import ConfigParser
from utils.random_utils import randint_array


class Variables(object):
    """
    Variables of parameters
    """
    def __init__(self, base_stations=None, bs_number=None, bs_memory=None,
                 users=None, user_memory=None, user_number=None,
                 files=None, file_number=None, file_size=None,
                 zipf_a=None, bs_network=None, users_network=None,
                 distance_scale=None, radius=None,
                 p_b=None, p_0=None, sigma=None, beta_bu=None,
                 beta_0u=None, alpha=None, w=None):
        self.base_stations = base_stations
        self.bs_number = bs_number
        self.bs_memory = bs_memory
        self.users = users
        self.user_memory = user_memory
        self.user_number = user_number
        self.files = files
        self.file_number = file_number
        self.file_size = file_size
        self.zipf_a = zipf_a
        self.bs_network = bs_network
        self.users_network = users_network
        self.distance_scale = distance_scale
        self.radius = radius
        self.p_b = p_b
        self.p_0 = p_0
        self.sigma = sigma
        self.beta_bu = beta_bu
        self.beta_0u = beta_0u
        self.alpha = alpha
        self.w = w

    @classmethod
    def from_(cls, cfg_file=None):
        """
        Parse variables

        Args:
            cfg_file(str): cfg file name
        """
        cfg_file = cfg_file if cfg_file is not None else 'basic.cfg'
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_path = '{}/cfg/{}'.format(current_path, cfg_file)
        config = ConfigParser.RawConfigParser()
        config.readfp(open(config_path))

        bs_number = int(config.get('base stations', 'number'))
        bs_memory = int(config.get('base stations', 'memory'))
        base_stations = range(bs_number)
        user_number = int(config.get('users', 'number'))
        users = range(user_number)
        user_memory = int(config.get('users', 'memory'))
        file_number = int(config.get('files', 'number'))
        lowest_size = int(config.get('files', 'lowest_size'))
        highest_size = int(config.get('files', 'highest_size'))
        files = range(file_number)
        file_size = randint_array(low_bound=lowest_size, up_bound=highest_size, size=file_number)

        bs_network = '/'.join([current_path, config.get('network', 'bs_network')])
        users_network = '/'.join([current_path, config.get('network', 'users_network')])
        distance_scale = float(config.get('network', 'distance_scale'))
        radius = float(config.get('network', 'radius'))

        zipf_a = float(config.get('zipf', 'zipf_a'))

        p_b = float(config.get('sinr', 'p_b'))
        p_0 = float(config.get('sinr', 'p_0'))
        sigma = float(config.get('sinr', 'sigma'))
        beta_bu = float(config.get('sinr', 'beta_bu'))
        beta_0u = float(config.get('sinr', 'beta_0u'))
        alpha = float(config.get('sinr', 'alpha'))
        W = float(config.get('sinr', 'W'))

        params = {
            'base_stations': base_stations,
            'bs_number': bs_number,
            'bs_memory': bs_memory,
            'users': users,
            'user_number': user_number,
            'user_memory': user_memory,
            'files': files,
            'file_number': file_number,
            'file_size': file_size,
            'zipf_a': zipf_a,
            'bs_network': bs_network,
            'users_network': users_network,
            'distance_scale': distance_scale,
            'radius': radius,
            'p_b': p_b,
            'p_0': p_0,
            'sigma': sigma,
            'beta_bu': beta_bu,
            'beta_0u': beta_0u,
            'alpha': alpha,
            'w': W
        }

        return cls(**params)

    def to_dict(self):
        """
        To dict
        """
        return self.__dict__


if __name__ == '__main__':
    v = Variables.from_()
    print v.to_dict()
