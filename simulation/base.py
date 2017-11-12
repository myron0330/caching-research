# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from caching.agent import Agent
from caching.algorithms.lp_solvers import primal_dual_recover
from display.rewards import display_single_


def simulate_with_(algorithm, config=None, circles=200, dump=True, optimal=False, **kwargs):
    """
    Simulate with parameters.
    Args:
        algorithm(function): algorithm
        config(string): config path
        circles(int): circles
        dump(boolean): whether to dump result to file
        optimal(boolean): whether to find the optimal
    """
    config = config or '../etc/default.cfg'
    agent = Agent.from_(config)
    if optimal:
        algorithm_rewards = agent.find_optimal_with_bnd_(algorithm, circles=circles, dump=dump)
    else:
        algorithm_rewards = agent.iter_with_(algorithm, circles=circles, dump=dump)
    return algorithm_rewards


if __name__ == '__main__':
    config_path = '../etc/myron.cfg'
    current_algorithm = primal_dual_recover
    # current_algorithm = branch_and_bound
    rewards = simulate_with_(current_algorithm, config=config_path, circles=30,
                             dump=False, optimal=False)
    display_single_(rewards, all_curves=False, display_length=500, line_width=1.8,
                    title_size=20, label_size=16, color='#1E90FF')
