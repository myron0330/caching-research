# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from . base import simulate_with_


def algorithm_comparison(algorithms, config=None, dump=True):
    """
    Algorithm comparison
    :param algorithms:
    :return:
    """


if __name__ == '__main__':
    config_path = '../etc/algo_comp.cfg'
    current_algorithm = primal_dual_recover
    # current_algorithm = branch_and_bound
    rewards = simulate_with_(current_algorithm, config=config_path, circles=30,
                             dump=False, optimal=False)
    display_single_(rewards, all_curves=False, length=500, line_width=1.8,
                    title_size=20, label_size=16, color='#1E90FF')
