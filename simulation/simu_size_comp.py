# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from __future__ import division
import pickle
import numpy as np
import pandas as pd
from os import listdir
from collections import OrderedDict
from caching.algorithms import primal_dual_recover, lfu, lru, branch_and_bound
from display_rewards.rewards import display_multiple_
from simulation.base import simulate_with_
from caching.utils.dict_utils import DefaultDict
from caching.variables import Variables


algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'Proposed algorithm',
    'lfu': 'LFU',
    'lru': 'LRU'
}


def size_comparison(algorithm, circles=200, dump=True, display=True, algorithm_type='original',
                    prefix='', **plot_kwargs):
    """
    Algorithm comparison

    Args:
        algorithm(function): algorithm
        circles(int): circles
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
        algorithm_type(string): algorithm type
        prefix(string): prefix
    """
    configs = filter(lambda x: x.startswith('sizes_comparison'), listdir('../etc'))
    rewards_dict = dict()
    for config in configs:
        key = 'Size-{}'.format(config.split('_')[-1]).split('.')[0]
        rewards_dict[key] = simulate_with_(algorithm, config=config, circles=circles,
                                           dump=dump, algorithm_type=algorithm_type,
                                           prefix=prefix, fixed_theta=True)
    if display:
        display_multiple_(rewards_dict, **plot_kwargs)
    return rewards_dict


def display_memory_comparison_by_(prefix, **plot_kwargs):
    """
    Display memory comparison.

    Args:
        prefix(prefix): prefix string
    """
    pks = sorted(filter(lambda x: x.startswith(prefix), listdir('../performance')),
                 key=lambda x: int(x.split('-')[2]), reverse=True)
    rewards_dict = OrderedDict()
    for pk in pks:
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))
        key = 'Memory-{}'.format(pk.split('-')[2])
        rewards_dict[key] = rewards
    display_multiple_(rewards_dict, **plot_kwargs)


def display_sizes_iteration(prefix, **plot_kwargs):
    """
    Display memory comparison
    """
    pks = []
    if isinstance(prefix, (str, unicode)):
        prefix = [prefix]
    for pre in prefix:
        pks += sorted(filter(lambda x: x.startswith(pre), listdir('../performance')),
                      key=lambda x: int(x.split('-')[2]), reverse=False)
    rewards_dict = OrderedDict()
    x_axis = list()
    for pk in sorted(pks, key=lambda x: int(x.split('-')[1])):
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))[150:]
        frame = pd.DataFrame(rewards).head(100)
        key = pk.split('.')[2]
        x_axis.append(int(pk.split('-')[1]))
        rewards_dict.setdefault(algorithm_mapper[key], list())
        rewards_dict[algorithm_mapper[key]].append(frame.sum(axis=1).mean())
    results = OrderedDict()
    for key in rewards_dict.keys():
        results[key] = sorted(rewards_dict[key], reverse=True)
    # results = rewards_dict
    plot_kwargs['x_axis'] = []
    for _ in x_axis:
        if _ not in plot_kwargs['x_axis']:
            plot_kwargs['x_axis'].append(_)
    display_multiple_(results, **plot_kwargs)


def compare_sizes_with_(algorithms, circles=100, dump=False, display=False, prefix='', **plot_parameters):
    for current_algorithm in algorithms:
        if current_algorithm == branch_and_bound:
            size_comparison(algorithm=branch_and_bound, circles=circles, dump=dump,
                            algorithm_type='optimal', display=display, prefix=prefix,
                            **plot_parameters)
        elif current_algorithm == primal_dual_recover:
            size_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                            algorithm_type='original', display=display, prefix=prefix,
                            **plot_parameters)
        else:
            size_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                            algorithm_type='comparison', display=display, prefix=prefix,
                            **plot_parameters)


def plot_sizes_comparison():
    parameters = {
        'display_length': 100,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 18,
        'marker': '',
        'marker_size': 8,
        'x_label': u'',
        'y_label': u'',
        'with_standardize': True,
        'standardize_init': 2,
        'standardize_special': False,
        'sigma': 0.5,
        'legend_size': 15,
        'y_min_lim': 200,
        'loc': 4,
        'texts': [
            {
                'args': (55, 187, '$K$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (4.8, 300, '$\\overline{R}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/sizes_comparison.jpg'
    }
    display_sizes_iteration(['sizes.rewards.branch_and_bound.fixed.5-',
                             'sizes.rewards.primal_dual_recover.5-',
                             'sizes.rewards.lfu.5-',
                             'sizes.rewards.lru.5-'
                             ], **parameters)


if __name__ == '__main__':
    plot_parameters = {
        'display_length': 100,
        'line_width': 2,
        'title_size': 20,
        'label_size': 18,
        'marker': '',
        'marker_size': 8,
        'x_label': u'',
        'y_label': u'',
        'with_standardize': True,
        'standardize_init': 10,
        'sigma': 1.5,
        'save_path': '../plots/sizes_comparison.jpg'
    }
    # compare_sizes_with_(algorithms=[primal_dual_recover],
    #                     circles=200, dump=True, prefix='sizes', display=False,
    #                     **plot_parameters)
    # display_memory_comparison_by_('rewards.primal_dual_recover.4-20-', **plot_parameters)
    # display_memory_iteration(['rewards.branch_and_bound.dynamic.4-20-',
    #                           'rewards.primal_dual_recover.4-20-',
    #                           'rewards.lfu.4-20-',
    #                           'rewards.lru.4-20-',
    #                           ], **plot_parameters)
    # algorithms = [primal_dual_recover, branch_and_bound, lfu, lru]
    # compare_memories_with_(algorithms, circles=100, dump=True, display=False)
    # plot_memory_comparison()
    # display_sizes_iteration(prefix='sizes.', **plot_parameters)
    plot_sizes_comparison()
