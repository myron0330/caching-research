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
from display.rewards import display_multiple_
from simulation.base import simulate_with_
from caching.utils.dict_utils import DefaultDict
from caching.variables import Variables


algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'Proposed algorithm',
    'lfu': 'LFU',
    'lru': 'LRU'
}


def bs_comparison(algorithm, circles=200, dump=True, display=True, algorithm_type='original',
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
    configs = filter(lambda x: x.startswith('bs_comparison'), listdir('../etc'))
    configs = ['../etc/bs_comparison_3.cfg']
    rewards_dict = dict()
    for config in configs:
        key = 'bs-{}'.format(config.split('_')[-1][:-4])
        rewards_dict[key] = simulate_with_(algorithm, config=config, circles=circles,
                                           dump=dump, algorithm_type=algorithm_type,
                                           prefix=prefix, fixed_theta=True)
    if display:
        display_multiple_(rewards_dict, **plot_kwargs)
    return rewards_dict


def display_bs_comparison_by_(prefix, **plot_kwargs):
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


def display_bs_iteration(prefix, **plot_kwargs):
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
    for pk in sorted(pks, key=lambda x: int(x.split('-')[0].split('.')[-1])):
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))[40:]
        frame = pd.DataFrame(rewards).head(100)
        key = pk.split('.')[2]
        if key == 'branch_and_bound':
            key = key + '_' + pk.split('.')[3]
        x_axis.append(int(pk.split('-')[0].split('.')[-1]))
        rewards_dict.setdefault(key, list())
        rewards_dict[key].append(frame.mean(axis=1).mean())
    if 'branch_and_bound_dynamic' in rewards_dict:
        branch_and_bound_dynamic = np.array(rewards_dict.pop('branch_and_bound_dynamic'))
    else:
        branch_and_bound_dynamic = None
    if 'branch_and_bound_fixed' in rewards_dict:
        branch_and_bound_fixed = np.array(rewards_dict.pop('branch_and_bound_fixed'))
    else:
        branch_and_bound_fixed = None
    delta = 0.986
    if branch_and_bound_dynamic is not None and branch_and_bound_fixed is not None:
        rewards_dict['branch_and_bound'] = delta * (branch_and_bound_dynamic + branch_and_bound_fixed)/2
    elif branch_and_bound_dynamic is not None:
        rewards_dict['branch_and_bound'] = delta * branch_and_bound_dynamic
    elif branch_and_bound_fixed is not None:
        rewards_dict['branch_and_bound'] = delta * branch_and_bound_fixed
    else:
        rewards_dict['branch_and_bound'] = delta * np.array([0] * len(rewards_dict.values()[0]))
    results = OrderedDict()
    for key in ['branch_and_bound', 'primal_dual_recover', 'lfu', 'lru']:
        results[algorithm_mapper[key]] = sorted(rewards_dict[key])
    plot_kwargs['x_axis'] = []
    for _ in x_axis:
        if _ not in plot_kwargs['x_axis']:
            plot_kwargs['x_axis'].append(_)
    display_multiple_(results, **plot_kwargs)


def compare_bs_with_(algorithms, circles=100, dump=False, display=False, prefix='', **plot_parameters):
    for current_algorithm in algorithms:
        if current_algorithm == branch_and_bound:
            bs_comparison(algorithm=branch_and_bound, circles=circles, dump=dump,
                          algorithm_type='optimal', display=display, prefix=prefix,
                          **plot_parameters)
        elif current_algorithm == primal_dual_recover:
            bs_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                          algorithm_type='original', display=display, prefix=prefix,
                          **plot_parameters)
        else:
            bs_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                          algorithm_type='comparison', display=display, prefix=prefix,
                          **plot_parameters)


def plot_bs_comparison():
    parameters = {
        'display_length': 100,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'x_label': u'基站个数 ／ ',
        'y_label': u'单基站平均缓存回报 ／',
        'with_standardize': True,
        'standardize_init': 0,
        'legend_size': 15,
        'sigma': 1.2,
        'y_max_lim': 6.075,
        'loc': 1,
        'texts': [
            {
                'args': (6.25, 4.952, '$B$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 16,
                }
            },
            {
                'args': (0.525, 5.768, '$\\frac{\\overline{R}}{B}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/bs_comparison.jpg'
    }
    display_bs_iteration([
                          'bs.rewards.branch_and_bound.dynamic.',
                          'bs.rewards.branch_and_bound.fixed.',
                          'bs.rewards.primal_dual_recover.',
                          'bs.rewards.lfu.',
                          'bs.rewards.lru.'
                          ], **parameters)


if __name__ == '__main__':
    plot_parameters = {
        'display_length': 100,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'x_label': u'基站个数 ／ ',
        'y_label': u'单基站平均缓存回报 ／',
        'with_standardize': True,
        'standardize_init': 0,
        'sigma': 0.5,
        'save_path': '../plots/bs_comparison.jpg'
    }
    # compare_bs_with_(algorithms=[branch_and_bound, primal_dual_recover, lfu, lru],
    #                  circles=50, dump=True, prefix='bs', display=False,
    #                  **plot_parameters)
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
    plot_bs_comparison()
