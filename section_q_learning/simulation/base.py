# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from section_q_learning.agent import Agent
from section_q_learning.algorithms.lp_solvers import primal_dual_recover
from section_q_learning.display.rewards import display_single_


def simulate_with_(algorithm, config=None, circles=200, dump=True,
                   algorithm_type='original', fixed_theta=False, prefix='', **kwargs):
    """
    Simulate with parameters.

    Args:
        algorithm(function): algorithm
        config(string): config path
        circles(int): circles
        dump(boolean): whether to dump result to file
        algorithm_type(string): original, optimal, comparison
        fixed_theta(boolean): fixed theta
        prefix(string): prefix
    """
    config = config or '../cfg/default.cfg'
    agent = Agent.from_(config)
    if algorithm_type == 'optimal':
        algorithm_rewards = agent.find_optimal_with_bnd_(primal_dual_recover, circles=circles, dump=dump,
                                                         fixed_theta=fixed_theta,
                                                         prefix=prefix)
    elif algorithm_type == 'original':
        algorithm_rewards = agent.iter_with_(algorithm, circles=circles, dump=dump, prefix=prefix)
    elif algorithm_type == 'greedy':
        algorithm_rewards = agent.iter_with_greedy_(algorithm, circles=circles, dump=dump, prefix=prefix)
    elif algorithm_type == 'global_q_learning':
        algorithm_rewards = agent.iter_with_q_learning_(algorithm, circles=circles, dump=dump, prefix=prefix)
    else:
        algorithm_rewards = agent.comparison_(algorithm, circles=circles, dump=dump, prefix=prefix)
    return algorithm_rewards


if __name__ == '__main__':
    config_path = '../cfg/myron.cfg'
    current_algorithm = primal_dual_recover
    # current_algorithm = branch_and_bound
    rewards = simulate_with_(current_algorithm, config=config_path, circles=30,
                             dump=False)
    display_single_(rewards, all_curves=False, display_length=500, line_width=1.8,
                    title_size=20, label_size=16, color='#1E90FF')
