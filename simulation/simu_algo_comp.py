# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from caching.algorithms import branch_and_bound, primal_dual_recover
from display.rewards import display_multiple_
from simulation.base import simulate_with_


def algorithm_comparison(algorithms, comparison_algorithm=None,
                         circles=200, dump=True,
                         display=True, display_length=30):
    """
    Algorithm comparison

    Args:
        algorithms(list): algorithm
        comparison_algorithm(function): comparison algorithm
        circles(int): circles
        dump(boolean): whether to dump result to file
        display(boolean): whether to display
        display_length(int): display length
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
        display_multiple_(rewards_dict, display_length=display_length, line_width=2, title_size=20,
                          label_size=16, marker='*', marker_size=3)
    return rewards_dict


if __name__ == '__main__':
    t_algorithms = [primal_dual_recover]
    t_comparison_algorithm = primal_dual_recover
    algorithm_comparison(t_algorithms, comparison_algorithm=t_comparison_algorithm,
                         circles=100, dump=False)