# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from caching.agent import Agent
from caching.algorithms.core import primal_dual_recover
from display.rewards import display_single_


def simulate_with_(run=False, circles=200, **kwargs):
    """
    Simulate with parameters.

    Args:
        run(boolean): whether to run new algorithm
        circles(int): circles
    """
    if run:
        config = '../etc/default.cfg'
        agent = Agent.from_(config)
        agent.iter_with_(primal_dual_recover, circles=circles)
    rewards = pickle.load(open('../performance/rewards.pk', 'r+'))
    display_single_(rewards, **kwargs)


if __name__ == '__main__':
    simulate_with_(run=True, circles=1000, all_curves=False, length=200, line_width=1.8,
                   title_size=20, label_size=16, color='#1E90FF')
