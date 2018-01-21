# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def plot_network(fig_size=None, users_network=None, bs_network=None, dump=False, save_path=None):
    """
    Plot network topology.
    Args:
        fig_size(tuple): figure size
        users_network(obj): Network object of users
        bs_network(obj): Network object of base stations
        dump(boolean): whether to save the picture
        save_path(string): save path

    Returns:

    """
    fig = plt.figure(figsize=fig_size)
    axes = fig.add_subplot(111)
    nx.draw(users_network, pos=users_network.positions_info, with_labels=False, node_size=10, width=0, node_color='k')
    nx.draw(bs_network, pos=bs_network.positions_info, with_labels=False, node_size=50, width=0, node_color='r')
    theta = np.arange(0, 2*np.pi, 0.01)
    r = 1.1
    for bs, position_info in bs_network.positions_info.iteritems():
        x = position_info[0] + r * np.cos(theta)
        y = position_info[1] + r * np.sin(theta)
        axes.plot(x, y, color='k')
        axes.axis('equal')

    if dump:
        save_path = save_path or '../plots/network_topology.jpg'
        plt.savefig(save_path)
    plt.show()


if __name__ == '__main__':
    plot_parameters = {
        'fig_size': (6, 6),
        'users_network': pickle.load(open('../resources/users_network.pk', 'r+')),
        'bs_network': pickle.load(open('../resources/bs_network.pk', 'r+')),
        'dump': True
    }
    plot_network(**plot_parameters)
