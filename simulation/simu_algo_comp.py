# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
import numpy as np
import pandas as pd
from collections import OrderedDict
from caching.algorithms import *
from display.rewards import display_multiple_, display_single_
from simulation.base import simulate_with_


algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'Proposed algorithm',
    'lfu': 'LFU',
    'lru': 'LRU'
}


def algorithm_comparison(algorithms, comparison_algorithm=None,
                         circles=200, dump=True, fixed_theta=False,
                         display=True, prefix='', **plot_kwargs):
    """
    Algorithm comparison

    Args:
        algorithms(list): algorithm
        comparison_algorithm(function): comparison algorithm
        circles(int): circles
        fixed_theta(boolean): fixed theta
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
        prefix(string): prefix
    """
    config = '../etc/algorithm_comparison.cfg'
    rewards_dict = OrderedDict()
    if comparison_algorithm:
        rewards_dict[branch_and_bound.func_name] = simulate_with_(comparison_algorithm, config=config, circles=circles,
                                                                  dump=dump, algorithm_type='optimal', prefix=prefix,
                                                                  fixed_theta=fixed_theta)
        # rewards_dict['greedy'] = simulate_with_(comparison_algorithm, config=config, circles=circles,
        #                                         dump=dump, algorithm_type='greedy')
    for algorithm in algorithms:
        rewards_dict[algorithm.func_name] = simulate_with_(algorithm, config=config, circles=circles, prefix=prefix,
                                                           dump=dump)
    rewards_dict[lfu.func_name] = simulate_with_(lfu, config=config, circles=circles, dump=dump, prefix=prefix,
                                                 algorithm_type='comparison')
    rewards_dict[lru.func_name] = simulate_with_(lru, config=config, circles=circles, dump=dump, prefix=prefix,
                                                 algorithm_type='comparison')
    if display:
        display_multiple_(rewards_dict, **plot_kwargs)
    return rewards_dict


def display_algorithm_comparison_by_(file_names, **plot_kwargs):
    """
    Display memory comparison.

    Args:
        file_names(list): file names
    """
    rewards_dict = OrderedDict()
    for file_name in file_names:
        rewards = pickle.load(open('../performance/{}'.format(file_name), 'r+'))
        key = file_name.split('.')[2]
        rewards_dict[algorithm_mapper[key]] = rewards
    display_multiple_(rewards_dict, **plot_kwargs)


def display_single_algorithm_by_(file_name, **plot_kwargs):
    """
    Display memory comparison.

    Args:
        file_name(string): file names
    """
    rewards_dict = OrderedDict()
    rewards = pickle.load(open('../performance/{}'.format(file_name), 'r+'))
    key = file_name.split('.')[1]
    rewards_dict[key] = rewards
    display_single_(rewards, **plot_kwargs)


def display_regret_by_(file_names, **plot_kwargs):
    """
    Display regret comparison
    :param file_names:
    :param plot_kwargs:
    :return:
    """
    rewards_dict = OrderedDict()
    for file_name in file_names:
        rewards = pickle.load(open('../performance/{}'.format(file_name), 'r+'))
        key = file_name.split('.')[1]
        frame = pd.DataFrame(rewards)
        frame['total'] = frame.sum(axis=1)
        frame['cumulative'] = frame['total'].cumsum()
        rewards_dict[algorithm_mapper[key]] = np.array(frame['cumulative'])
    benchmark = rewards_dict.pop('B&B')
    regrets = OrderedDict()
    slots = 50
    for key, value in rewards_dict.iteritems():
        regrets[key] = list(np.log10(benchmark - value))[::slots]
    x_axis = map(lambda x: x * 50, range(len(regrets.values()[0])))
    plot_kwargs['x_axis'] = x_axis
    display_multiple_(regrets, **plot_kwargs)
    return rewards_dict


def plot_algorithms_comparison():
    parameters = {
        'display_length': 50,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'迭代次数 / ',
        'y_label': u'缓存回报 / ',
        'all_curves': True,
        'with_standardize': True,
        'standardize_init': 19,
        'sigma': 0.75,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (28.5, -1.45, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 16,
                }
            },
            {
                'args': (-2.15, 14.5, '$R$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 16,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/algorithms_comparison.jpg',
    }
    display_algorithm_comparison_by_(['algorithm.rewards.branch_and_bound.fixed.5-20-100-20-2.0.pk',
                                      'algorithm.rewards.primal_dual_recover.5-20-100-20-2.0.pk',
                                      'algorithm.rewards.lfu.5-20-100-20-2.0.pk',
                                      'algorithm.rewards.lru.5-20-100-20-2.0.pk'], **parameters)
    return None


def plot_regrets_comparison():
    parameters = {
        'display_length': 100,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'迭代次数 / ',
        'y_label': u'对数化损失 / ',
        'all_curves': True,
        'with_standardize': False,
        'standardize_init': 6,
        'sigma': 3,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (1115, -0.28, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 16,
                }
            },
            {
                'args': (-65, 3.15, '$Log(reg)$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 16,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/regrets_comparison.jpg',
    }
    display_regret_by_(['algorithm.rewards.branch_and_bound.fixed.5-20-100-20-2.0.pk',
                        'algorithm.rewards.primal_dual_recover.5-20-100-20-2.0.pk',
                        'algorithm.rewards.lfu.5-20-100-20-2.0.pk',
                        'algorithm.rewards.lru.5-20-100-20-2.0.pk'], **parameters)


if __name__ == '__main__':
    plot_parameters = {
        'display_length': 50,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'迭代次数 / t',
        'y_label': u'回报 / R',
        'all_curves': True,
        'with_standardize': False,
        'standardize_init': 6,
        'sigma': 3,
        'loc': 4,
        'legend_size': 12,
        'fixed_theta': True,
        'y_min_lim': 0,
        'save_path': '../plots/regrets_comparison.jpg',
        # 'save_path': '../plots/algorithms_comparison.jpg',
    }
    t_algorithms = [primal_dual_recover]
    t_comparison_algorithm = primal_dual_recover
    algorithm_comparison(t_algorithms, comparison_algorithm=t_comparison_algorithm, prefix='algorithm',
                         circles=2000, dump=True, **plot_parameters)
    plot_algorithms_comparison()
    # plot_regrets_comparison()
