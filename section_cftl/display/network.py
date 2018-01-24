# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def plot_network(fig_size=None, users_network=None, bs_network=None,
                 dump=False, save_path=None, x_lim=None, y_lim=None,
                 radius=1):
    """
    Plot network topology.
    Args:
        fig_size(tuple): figure size
        users_network(obj): Network object of users
        bs_network(obj): Network object of base stations
        dump(boolean): whether to save the picture
        save_path(string): save path
        x_lim(tuple): x lim
        y_lim(tuple): y lim
        radius(float): radius

    Returns:

    """
    fig = plt.figure(figsize=fig_size)
    axes = fig.add_subplot(111)
    axes.spines['left'].set_color('black')
    axes.spines['right'].set_color('black')
    axes.spines['top'].set_color('black')
    axes.spines['bottom'].set_color('black')
    nx.draw(users_network, pos=users_network.positions_info, with_labels=False, node_size=10, width=0, node_color='k')
    nx.draw(bs_network, pos=bs_network.positions_info, with_labels=False, node_size=50, width=0, node_color='r')
    theta = np.arange(0, 2*np.pi, 0.01)
    r = radius
    for bs, position_info in bs_network.positions_info.iteritems():
        x = position_info[0] + r * np.cos(theta)
        y = position_info[1] + r * np.sin(theta)
        axes.plot(x, y, color='k')
        axes.axis('equal')
    if x_lim is not None:
        plt.xlim(*x_lim)
    if y_lim is not None:
        plt.ylim(*y_lim)
    if dump:
        save_path = save_path or '../plots/network_topology.jpg'
        plt.savefig(save_path)
    plt.show()
