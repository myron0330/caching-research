# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from __future__ import division

import pickle
from collections import OrderedDict
from os import listdir
import pandas as pd
from section_cmab.display.rewards import display_multiple_
from section_cmab.algorithms import primal_dual_recover, branch_and_bound
from section_cmab.simulation.base import simulate_with_
from section_cmab.variables import Variables

algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'Proposed algorithm',
    'lfu': 'LFU',
    'lru': 'LRU'
}


def memory_comparison(algorithm, circles=200, dump=True, display=True, algorithm_type='original',
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
    configs = filter(lambda x: x.startswith('memory_comparison'), listdir('../etc'))
    # configs = ['memory_comparison_25.cfg']
    rewards_dict = dict()
    for config in configs:
        key = 'Memory-{}'.format(config.split('_')[-1]).split('.')[0]
        rewards_dict[key] = simulate_with_(algorithm, config=config, circles=circles, prefix=prefix, fixed_theta=True,
                                           dump=dump, algorithm_type=algorithm_type)
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


def display_memory_iteration(prefix, **plot_kwargs):
    """
    Display memory comparison
    """
    variables = Variables.from_('../cfg/memory_comparison_50.cfg')
    total_sizes = sum(variables.sizes)
    pks = []
    if isinstance(prefix, (str, unicode)):
        prefix = [prefix]
    for pre in prefix:
        pks += sorted(filter(lambda x: x.startswith(pre), listdir('../performance')),
                      key=lambda x: int(x.split('-')[2]), reverse=False)
    file_number = int(pks[0].split('-')[1])
    rewards_dict = OrderedDict()
    x_axis = sorted(set(map(lambda x: int(x.split('-')[2]) / total_sizes, pks)))
    for pk in pks:
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))[file_number:]
        frame = pd.DataFrame(rewards).head(100)
        key = pk.split('.')[2]
        rewards_dict.setdefault(algorithm_mapper[key], list())
        rewards_dict[algorithm_mapper[key]].append(frame.sum(axis=1).mean())
    for key, value in rewards_dict.iteritems():
        rewards_dict[key] = sorted(value)
    plot_kwargs['x_axis'] = x_axis
    display_multiple_(rewards_dict, **plot_kwargs)


def compare_memories_with_(algorithms, circles=100, dump=False, display=False, **plot_parameters):
    for current_algorithm in algorithms:
        if current_algorithm == branch_and_bound:
            memory_comparison(algorithm=branch_and_bound, circles=circles, dump=dump,
                              algorithm_type='optimal', display=display,
                              **plot_parameters)
        elif current_algorithm == primal_dual_recover:
            memory_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                              algorithm_type='original', display=display,
                              **plot_parameters)
        else:
            memory_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                              algorithm_type='comparison', display=display,
                              **plot_parameters)


def plot_memory_comparison():
    parameters = {
        'display_length': 100,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'x_label': u'',
        'y_label': u'',
        'with_standardize': True,
        'standardize_init': 0,
        'sigma': 2.5,
        'legend_size': 15,
        'texts': [
            {
                'args': (0.6, 92, '$\\lambda$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (0.025, 275, '$\\overline{R}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/memory_comparison.jpg'

    }
    display_memory_iteration(['memory.rewards.branch_and_bound.fixed.5-20-',
                              'memory.rewards.primal_dual_recover.5-20-',
                              'memory.rewards.lfu.5-20-',
                              'memory.rewards.lru.5-20-',
                              ], **parameters)


if __name__ == '__main__':
    # plot_parameters = {
    #     'display_length': 100,
    #     'line_width': 2,
    #     'title_size': 20,
    #     'label_size': 16,
    #     'marker': '',
    #     'marker_size': 8,
    #     'x_label': u'存储容量',
    #     'y_label': u'平均缓存回报',
    #     'with_standardize': True,
    #     'standardize_init': 10,
    #     'sigma': 1.5,
    #     'save_path': '../plots/memory_comparison.jpg'
    #
    # }
    # memory_comparison(algorithm=branch_and_bound, circles=100, dump=True, algorithm_type='optimal',
    #                   **plot_parameters)
    # display_memory_comparison_by_('rewards.primal_dual_recover.4-20-', **plot_parameters)
    # display_memory_iteration(['rewards.branch_and_bound.dynamic.4-20-',
    #                           'rewards.primal_dual_recover.4-20-',
    #                           'rewards.lfu.4-20-',
    #                           'rewards.lru.4-20-',
    #                           ], **plot_parameters)
    # algorithms = [primal_dual_recover, branch_and_bound, lfu, lru]
    # compare_memories_with_(algorithms, circles=100, dump=True, prefix='memory', display=False)
    plot_memory_comparison()
