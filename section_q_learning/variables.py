# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: global variables
# **********************************************************************************#
import ConfigParser
import os
from utils.random_utils import randint_array


class Variables(object):
    """
    Variables of parameters
    """
    def __init__(self, bs_number=None, bs_memory=None, file_number=None, lowest_size=None, highest_size=None,
                 base_stations=None, users=None, user_size=None, files=None, sizes=None, file_info=None,
                 v_bd=None, v_bb=None, v_cb=None, zipf_a=None, beta=None, alpha=None):
        self.bs_number = bs_number
        self.bs_memory = bs_memory
        self.file_number = file_number
        self.lowest_size = lowest_size
        self.highest_size = highest_size
        self.base_stations = base_stations
        self.users = users
        self.user_size = user_size
        self.files = files
        self.sizes = sizes
        self.file_info = file_info
        self.v_bd = v_bd
        self.v_bb = v_bb
        self.v_cb = v_cb
        self.zipf_a = zipf_a
        self.beta = beta
        self.alpha = alpha

    @classmethod
    def from_(cls, cfg_file=None):
        """
        Parse variables

        Args:
            cfg_file(str): cfg file name
        """
        cfg_file = cfg_file if cfg_file is not None else 'default.cfg'
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_path = '{}/cfg/{}'.format(current_path, cfg_file)
        config = ConfigParser.RawConfigParser()
        config.readfp(open(config_path))

        bs_number = int(config.get('base stations', 'number'))
        bs_memory = int(config.get('base stations', 'memory'))
        user_size = int(config.get('users', 'size'))
        base_stations = range(bs_number)
        users = randint_array(low_bound=user_size, up_bound=user_size, size=bs_number)

        file_number = int(config.get('files', 'number'))
        lowest_size = int(config.get('files', 'lowest_size'))
        highest_size = int(config.get('files', 'highest_size'))
        files = range(file_number)
        sizes = randint_array(low_bound=lowest_size, up_bound=highest_size, size=file_number)
        file_info = dict(zip(files, sizes))

        v_bd = int(config.get('transmission rates', 'v_bd'))
        v_bb = int(config.get('transmission rates', 'v_bb'))
        v_cb = int(config.get('transmission rates', 'v_cb'))
        zipf_a = float(config.get('zipf', 'zipf_a'))

        beta = float(config.get('algorithm', 'beta'))
        alpha = float(config.get('algorithm', 'alpha'))
        params = {
            'bs_number': bs_number,
            'bs_memory': bs_memory,
            'user_size': user_size,
            'base_stations': base_stations,
            'users': users,
            'file_number': file_number,
            'lowest_size': lowest_size,
            'highest_size': highest_size,
            'files': files,
            'sizes': sizes,
            'file_info': file_info,
            'v_bd': v_bd,
            'v_bb': v_bb,
            'v_cb': v_cb,
            'zipf_a': zipf_a,
            'beta': beta,
            'alpha': alpha
        }
        return cls(**params)

    def to_dict(self):
        """
        To dict
        """
        return self.__dict__
