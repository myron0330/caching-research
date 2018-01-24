# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from section_cftl.display.network import plot_network


if __name__ == '__main__':
    plot_parameters = {
        'fig_size': (6, 6),
        'users_network': pickle.load(open('../resources/users_network.pk', 'r+')),
        'bs_network': pickle.load(open('../resources/bs_network.pk', 'r+')),
        'dump': False,
        'radius': 1.1,
        'x_lim': (-2.5, 2.5),
        'y_lim': (-2.5, 2.5)
    }
    plot_network(**plot_parameters)
