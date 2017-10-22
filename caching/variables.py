# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: global variables
# **********************************************************************************#
import os
import ConfigParser
from . utils.random_utils import randint_array


current_path = os.path.dirname(os.path.abspath(__file__))
config_path = '{}/../etc/research.cfg'.format(current_path)
config = ConfigParser.RawConfigParser()
config.readfp(open(config_path))


bs_number = int(config.get('base stations', 'number'))
bs_memory = int(config.get('base stations', 'memory'))
lowest_users = int(config.get('users', 'lowest_size'))
highest_users = int(config.get('users', 'highest_size'))
base_stations = range(bs_number)
users = randint_array(low_bound=lowest_users, high_bound=highest_users, size=bs_number)


file_number = int(config.get('files', 'number'))
lowest_size = int(config.get('files', 'lowest_size'))
highest_size = int(config.get('files', 'highest_size'))
files = range(file_number)
sizes = randint_array(low_bound=lowest_size, high_bound=highest_size, size=file_number)


v_bd = int(config.get('transmission rates', 'v_bd'))
v_bb = int(config.get('transmission rates', 'v_bb'))
v_cb = int(config.get('transmission rates', 'v_cb'))


__all__ = [
    'bs_number',
    'bs_memory',
    'file_number',
    'lowest_size',
    'highest_size',
    'base_stations',
    'users',
    'files',
    'sizes'
]
