# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from os import listdir
from collections import OrderedDict
from caching.algorithms import branch_and_bound, primal_dual_recover
from display.rewards import display_multiple_, display_single_
from simulation.base import simulate_with_


def algorithm_comparison(algorithms, comparison_algorithm=None,
                         circles=200, dump=True,
                         display=True, **plot_kwargs):
    """
    Algorithm comparison

    Args:
        algorithms(list): algorithm
        comparison_algorithm(function): comparison algorithm
        circles(int): circles
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
    """
    config = '../etc/algorithm_comparison.cfg'
    rewards_dict = dict()
    for algorithm in algorithms:
        rewards_dict[algorithm.func_name] = simulate_with_(algorithm, config=config,  circles=circles,
                                                           dump=dump, optimal=False)
    if comparison_algorithm:
        rewards_dict[branch_and_bound.func_name] = simulate_with_(comparison_algorithm, config=config, circles=circles,
                                                                  dump=dump, optimal=True)
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
        key = file_name.split('.')[1]
        rewards_dict[key] = rewards
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


if __name__ == '__main__':
    plot_parameters = {
        'display_length': 50,
        'line_width': 2,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': u'算法回报对比图',
        'x_label': u'迭代次数',
        'y_label': u'回报',
        'all_curves': True,
        'with_standardize': False,
        'standardize_init': 6,
        'sigma': 3,
    }
    t_algorithms = [primal_dual_recover]
    # t_comparison_algorithm = primal_dual_recover
    # algorithm_comparison(t_algorithms, comparison_algorithm=t_comparison_algorithm,
    #                      circles=100, dump=True, **plot_parameters)
    display_algorithm_comparison_by_(['rewards.branch_and_bound.4-6-15-300.pk',
                                      'rewards.primal_dual_recover.4-6-15-300.pk'], **plot_parameters)
    # display_single_algorithm_by_('rewards.branch_and_bound.4-6-15-300.pk', **plot_parameters)
