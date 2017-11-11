# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from caching.agent import Agent
from caching.algorithms.core import primal_dual_recover
from caching.algorithms.bnb import branch_and_bound
from display.rewards import display_single_


def simulate_with_(algorithm, run=False, config=None, circles=200, **kwargs):
    """
    Simulate with parameters.

    Args:
        algorithm(function): algorithm
        run(boolean): whether to run new algorithm
        config(string): config path
        circles(int): circles
    """
    if run:
        config = config or '../etc/default.cfg'
        agent = Agent.from_(config)
        agent.iter_with_(algorithm, circles=circles)
    rewards = pickle.load(open('../performance/rewards.pk', 'r+'))
    display_single_(rewards, **kwargs)


if __name__ == '__main__':
    config_path = '../etc/myron.cfg'
    # current_algorithm = primal_dual_recover
    current_algorithm = branch_and_bound
    simulate_with_(current_algorithm, run=True, config=config_path, circles=50, all_curves=False, length=500, line_width=1.8,
                   title_size=20, label_size=16, color='#1E90FF')
