# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from section_q_learning.display.network import plot_network


plot_parameters = {
    'fig_size': (6, 6),
    'bs_network': pickle.load(open('../resources/bs_network.pk', 'r+')),
    'dump': True,
    'width': 2,
    'node_size': 50,
    'node_color': 'r'
}
plot_network(**plot_parameters)
