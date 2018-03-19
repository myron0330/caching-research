# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def plot_network(fig_size=None, bs_network=None,
                 dump=False, save_path=None,
                 x_lim=None, y_lim=None,
                 width=1, node_size=50,
                 node_color='r'):
    """
    Plot network topology.
    Args:
        fig_size(tuple): figure size
        bs_network(obj): Network object of base stations
        dump(boolean): whether to save the picture
        save_path(string): save path
        x_lim(tuple): x lim
        y_lim(tuple): y lim
        width(float): edge width
        node_size(float): node size
        node_color(string): node color

    Returns:

    """
    fig = plt.figure(figsize=fig_size)
    axes = fig.add_subplot(111)
    axes.spines['left'].set_color('black')
    axes.spines['right'].set_color('black')
    axes.spines['top'].set_color('black')
    axes.spines['bottom'].set_color('black')
    nx.draw(bs_network, pos=bs_network.positions_info, with_labels=False,
            node_size=1100, width=0, edge_color='k', node_color='w', alpha=0.4)
    nx.draw(bs_network, pos=bs_network.positions_info, with_labels=False,
            node_size=node_size, width=width, node_color=node_color)
    if x_lim is not None:
        plt.xlim(*x_lim)
    if y_lim is not None:
        plt.ylim(*y_lim)
    if dump:
        save_path = save_path or '../plots/network_topology.jpg'
        plt.savefig(save_path)
    plt.show()
