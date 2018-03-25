# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from __future__ import division
import pickle
from collections import OrderedDict
from os import listdir
from section_cftl.agent import Agent
from section_cftl.algorithms.enums import Algorithm
from section_cftl.display.latency import display_latency


def decay_comparison(decay_range, circles=50, dump=True, prefix='decay'):
    """
    Decay comparison for proposed algorithm.

    Args:
        decay_range(list): decay range
        circles(int): iteration circles
        dump(boolean): whether to dump database
        prefix(string): prefix
    """
    agent = Agent.from_()
    for decay in decay_range:
        agent.iter_with_(Algorithm.proposed_algorithm, circles=circles, dump=dump,
                         prefix=prefix, decay=decay)


def display_latency_by_(**plot_kwargs):
    """
    Display latency by files and plot parameters.

    Args:
        **plot_kwargs: plot parameters
    """
    relative_path = '../performance'
    latencies = filter(lambda x: x.startswith('decay.'), listdir(relative_path))
    latency_data = OrderedDict()
    for latency in sorted(latencies):
        path = '/'.join([relative_path, latency])
        decay = latency.split('-')[-1][:-3]
        rewards = pickle.load(open(path, 'r+'))
        latency_data['$\\lambda = $' + decay] = rewards
    display_latency(latency_data, **plot_kwargs)


if __name__ == '__main__':
    # decay_comparison([0.6, 0.7, 0.8, 0.9])
    parameters = {
        'display_length': 100,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'',
        'y_label': u'',
        'loc': 'best',
        'legend_size': 15,
        'y_min_lim': 0,
        'y_max_lim': 200,
        'texts': [
            {
                'args': (25, -15, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-3.8, 100, '$f(\\bf{X}_t, y_t)$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/decay_comparison.jpg',
    }
    display_latency_by_(**parameters)
