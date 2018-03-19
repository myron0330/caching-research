# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
import numpy as np
import pandas as pd
from collections import OrderedDict
from os import listdir
from section_q_learning.algorithms import *
from section_q_learning.display.rewards import display_multiple_, display_single_
from section_q_learning.display.tools import display_dict_
from section_q_learning.simulation.base import simulate_with_

algorithm_mapper = {
    'branch_and_bound': 'B&B',
    'primal_dual_recover': 'CUCB-PE',
    'lfu': 'LFU',
    'lru': 'LRU',
    'global_q_learning': 'Q-learning'
}


def algorithm_comparison(algorithms, comparison_algorithm=None,
                         circles=200, dump=True, fixed_theta=False,
                         display=True, prefix='',
                         with_lfu=True, with_lru=True, **plot_kwargs):
    """
    Algorithm comparison

    Args:
        algorithms(list of func): algorithm
        comparison_algorithm(func): comparison algorithm
        circles(int): circles
        fixed_theta(boolean): fixed theta
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
        prefix(string): prefix
        with_lfu(boolean): with lfu or not
        with_lru(boolean): with lru or not
    """
    config = '../cfg/algorithm_comparison.cfg'
    rewards_dict = OrderedDict()
    if comparison_algorithm:
        rewards_dict[branch_and_bound.func_name] = simulate_with_(comparison_algorithm, config=config, circles=circles,
                                                                  dump=dump, algorithm_type='optimal', prefix=prefix,
                                                                  fixed_theta=fixed_theta)
        # rewards_dict['greedy'] = simulate_with_(comparison_algorithm, config=config, circles=circles,
        #                                         dump=dump, algorithm_type='greedy')
    for algorithm in algorithms:
        if algorithm.func_name == 'global_q_learning':
            algorithm_type = 'global_q_learning'
        else:
            algorithm_type = 'original'
        rewards_dict[algorithm.func_name] = simulate_with_(algorithm, config=config, circles=circles, prefix=prefix,
                                                           dump=dump, algorithm_type=algorithm_type)
    if with_lfu:
        rewards_dict[lfu.func_name] = simulate_with_(lfu, config=config, circles=circles, dump=dump, prefix=prefix,
                                                     algorithm_type='comparison')
    if with_lru:
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
        key = file_name.split('.')[2]
        file_number = int(file_name.split('-')[1])
        frame = pd.DataFrame(rewards).iloc[file_number:, :]
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
        'counter': 1,
        'with_q_values': False,
        'alpha': 0.2,
        'display_length': 50,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'',
        'y_label': u'',
        'all_curves': True,
        'with_standardize': True,
        'standardize_init': 19,
        'sigma': 0.5,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (25, -23.5, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-3.5, 200, '${R_t(S_{t-1}, C_t|\\Theta_t)}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/algorithms_comparison.jpg',
    }
    directory = listdir('../performance')
    files = filter(lambda x: x.startswith('algorithm.') and x.endswith('5-20-100-20-0.9.pk'), directory)
    display_algorithm_comparison_by_(files, **parameters)
    return None


def plot_q_values():
    parameters = {
        'with_q_values': True,
        'alpha': [0.05, 0.1, 0.2, 0.3, 0.4],
        'display_length': 50,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'',
        'y_label': u'',
        'all_curves': True,
        'with_standardize': True,
        'standardize_init': 20,
        'sigma': 0.6,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (25, -23.5, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-3.5, 200, '${\\hat{Q}_t(S_{t-1}, C_t)}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/q_values.jpg',
    }
    directory = listdir('../performance')
    files = filter(lambda x:
                   x.startswith('algorithm.rewards.global_q_learning')
                   and x.endswith('5-20-100-20-0.9.pk'), directory)
    display_algorithm_comparison_by_(files, **parameters)
    return None


def plot_regrets_comparison():
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
        'all_curves': True,
        'with_standardize': False,
        'standardize_init': 20,
        'sigma': 3,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (1000, -0.345, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-80, 3, '$Log(reg)$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/regrets_comparison.jpg',
    }
    files = filter(lambda x: x.startswith('algorithm.') and x.endswith('5-20-100-20-0.9.pk'), listdir('../performance'))
    display_regret_by_(files, **parameters)


def plots_cache_rate_comparison():
    """
    Cache rate comparison.
    """
    file_names = filter(lambda x: x.startswith('algorithm.c_bkt') and x.endswith('5-20-100-20-0.9.pk'),
                        listdir('../performance'))
    c_bkt_dict = OrderedDict()
    for file_name in file_names:
        c_bkt = pickle.load(open('../performance/{}'.format(file_name), 'r+'))
        algorithm_name = file_name.split('.')[2]
        c_bkt_dict[algorithm_mapper[algorithm_name]] = c_bkt
    file_names = filter(lambda x: x.startswith('algorithm.d_bkt') and x.endswith('5-20-100-20-0.9.pk'),
                        listdir('../performance'))
    d_bkt_dict = OrderedDict()
    for file_name in file_names:
        d_bkt = pickle.load(open('../performance/{}'.format(file_name), 'r+'))
        algorithm_name = file_name.split('.')[2]
        d_bkt_dict[algorithm_mapper[algorithm_name]] = d_bkt
    cache_rates = OrderedDict()
    for algorithm, c_bkt in c_bkt_dict.iteritems():
        d_bkt = d_bkt_dict[algorithm]
        rates = list()
        for _ in sorted(c_bkt):
            c = c_bkt[_]
            d = d_bkt[_]
            matrix = c * d
            cache_rate = matrix.sum() / d.sum()
            rates.append(cache_rate)
        avg_rates = rates[:1] + [np.average(rates[:_]) for _ in range(1, len(rates))]
        cache_rates[algorithm] = avg_rates
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
        'with_standardize': False,
        'standardize_init': 0,
        'sigma': 1.5,
        'loc': 4,
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'y_max_lim': 0.7,
        'counter': 3,
        'texts': [
            {
                'args': (500, -0.05, '$t$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-60, 0.35, '$\\overline{H}_{\\bf{1:t}}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 90,
                }
            }
        ],
        'save_path': '../plots/caching_rate.jpg',
    }
    display_dict_(data=cache_rates, **parameters)


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
    # t_algorithms = [primal_dual_recover]
    # # t_comparison_algorithm = global_q_learning
    # t_comparison_algorithm = None
    # algorithm_comparison(t_algorithms, comparison_algorithm=t_comparison_algorithm, prefix='algorithm',
    #                      circles=1000, dump=True, with_lfu=False, with_lru=False, **plot_parameters)
    # algorithm_comparison([primal_dual_recover], comparison_algorithm=primal_dual_recover, prefix='algorithm',
    #                      circles=2000, dump=True, **plot_parameters)
    plot_algorithms_comparison()
    plot_q_values()
    plots_cache_rate_comparison()
