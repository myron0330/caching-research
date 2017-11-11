# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from collections import OrderedDict
from os import listdir
from caching.algorithms import primal_dual_recover
from display.rewards import display_multiple_
from simulation.base import simulate_with_


def memory_comparison(algorithm, circles=200, dump=True, display=True, **plot_kwargs):
    """
    Algorithm comparison

    Args:
        algorithm(function): algorithm
        circles(int): circles
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
    """
    configs = filter(lambda x: x.startswith('memory_comparison'), listdir('../etc'))
    rewards_dict = dict()
    for config in configs:
        key = 'Memory-{}'.format(config.split('_')[-1]).split('.')[0]
        rewards_dict[key] = simulate_with_(algorithm, config=config, circles=circles, dump=dump, optimal=False)
    if display:
        display_multiple_(rewards_dict, **plot_kwargs)
    return rewards_dict


def display_memory_comparison(prefix, **plot_kwargs):
    """
    Display memory comparison.

    Args:
        prefix(prefix): prefix string
        display_length(int): length
    """
    pks = sorted(filter(lambda x: x.startswith(prefix), listdir('../performance')),
                 key=lambda x: int(x.split('-')[2]), reverse=True)
    rewards_dict = OrderedDict()
    for pk in pks:
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))
        key = 'Memory-{}'.format(pk.split('-')[2])
        rewards_dict[key] = rewards
    display_multiple_(rewards_dict, **plot_kwargs)

if __name__ == '__main__':
    plot_parameters = {
        'display_length': 200,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 3,
        'title': u'存储容量-回报对比图',
        'x_label': u'迭代次数',
        'y_label': u'回报'
    }
    # memory_comparison(algorithm=primal_dual_recover, circles=1000, dump=True, **plot_parameters)
    display_memory_comparison('rewards.primal_dual_recover.6-10-', **plot_parameters)
