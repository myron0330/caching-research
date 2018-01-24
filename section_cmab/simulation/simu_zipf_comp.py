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

algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'Proposed algorithm',
    'lfu': 'LFU',
    'lru': 'LRU'
}


def zipf_comparison(algorithm, circles=200, dump=True, display=True, algorithm_type='original',
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
    configs = filter(lambda x: x.startswith('zipf_comparison'), listdir('../etc'))
    # configs = ['../cfg/zipf_comparison_3.cfg']
    rewards_dict = dict()
    for config in configs:
        key = 'zipf-{}'.format(config.split('_')[-1][:-4])
        rewards_dict[key] = simulate_with_(algorithm, config=config, circles=circles,
                                           dump=dump, algorithm_type=algorithm_type, fixed_theta=True,
                                           prefix=prefix)
    if display:
        display_multiple_(rewards_dict, **plot_kwargs)
    return rewards_dict


def display_zipf_comparison_by_(prefix, **plot_kwargs):
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


def display_zipf_iteration(prefix, **plot_kwargs):
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
    for pk in pks:
        rewards = pickle.load(open('../performance/{}'.format(pk), 'r+'))[20:]
        frame = pd.DataFrame(rewards)
        key = pk.split('.')[2]
        x_axis.append(float(pk.split('-')[-1][:-3]))
        rewards_dict.setdefault(algorithm_mapper[key], list())
        rewards_dict[algorithm_mapper[key]].append(frame.sum(axis=1).mean())
    results = OrderedDict()
    for key in rewards_dict.keys():
        results[key] = sorted(rewards_dict[key])
    plot_kwargs['x_axis'] = []
    for _ in x_axis:
        if _ not in plot_kwargs['x_axis']:
            plot_kwargs['x_axis'].append(_)
    display_multiple_(results, **plot_kwargs)


def compare_zipf_with_(algorithms, circles=100, dump=False, display=False, prefix='', **plot_parameters):
    for current_algorithm in algorithms:
        if current_algorithm == branch_and_bound:
            zipf_comparison(algorithm=branch_and_bound, circles=circles, dump=dump,
                            algorithm_type='optimal', display=display, prefix=prefix,
                            **plot_parameters)
        elif current_algorithm == primal_dual_recover:
            zipf_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                            algorithm_type='original', display=display, prefix=prefix,
                            **plot_parameters)
        else:
            zipf_comparison(algorithm=current_algorithm, circles=circles, dump=dump,
                            algorithm_type='comparison', display=display, prefix=prefix,
                            **plot_parameters)


def plot_zipf_comparison():
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
        'standardize_init': 10,
        'legend_size': 15,
        'sigma': 1.5,
        'texts': [
            {
                'args': (1.3, 132, '$\\gamma$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (0.63, 275, '$\\overline{R}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/zipf_comparison.jpg'
    }
    display_zipf_iteration(['zipf.rewards.branch_and_bound.fixed.5-',
                            'zipf.rewards.primal_dual_recover.5-',
                            'zipf.rewards.lfu.5-',
                            'zipf.rewards.lru.5-'
                             ], **parameters)


if __name__ == '__main__':
    plot_parameters = {
        'display_length': 100,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'x_label': u'Zipf分布参数 ／ ',
        'y_label': u'平均缓存回报 ／',
        'with_standardize': True,
        'standardize_init': 100,
        'sigma': 1.5,
        'save_path': '../plots/zipf_comparison.jpg'
    }
    # algorithms = [primal_dual_recover, branch_and_bound, lfu, lru]
    # compare_zipf_with_(algorithms=algorithms,
    #                    circles=100, dump=True, prefix='zipf', display=False,
    #                    **plot_parameters)
    # display_memory_comparison_by_('rewards.primal_dual_recover.4-20-', **plot_parameters)
    # display_memory_iteration(['rewards.branch_and_bound.dynamic.4-20-',
    #                           'rewards.primal_dual_recover.4-20-',
    #                           'rewards.lfu.4-20-',
    #                           'rewards.lru.4-20-',
    #                           ], **plot_parameters)
    # plot_memory_comparison()
    # display_sizes_iteration(prefix='sizes.', **plot_parameters)
    plot_zipf_comparison()
