# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from section_cmab.agent import Agent
from section_cmab.algorithms.lp_solvers import primal_dual_recover
from latency_vs_rewards.rewards import display_single_


def simulate_with_(algorithm, run=False, config=None, circles=200, perf_file=None, optimal=False, **kwargs):
    """
    Simulate with parameters.

    Args:
        algorithm(function): algorithm
        run(boolean): whether to run new algorithm
        config(string): config path
        circles(int): circles
        perf_file(string): performance file
        optimal(boolean): whether to find the optimal

    """
    perf_file = perf_file or '../performance/rewards.pk'
    if run:
        config = config or '../cfg/default.cfg'
        agent = Agent.from_(config)
        if optimal:
            perf_file = agent.find_optimal_with_bnd_(algorithm, circles=circles)
        else:
            perf_file = agent.iter_with_(algorithm, circles=circles)
    rewards = pickle.load(open(perf_file, 'r+'))
    display_single_(rewards, **kwargs)


if __name__ == '__main__':
    config_path = '../cfg/algo_comp.cfg'
    current_algorithm = primal_dual_recover
    # current_algorithm = branch_and_bound
    simulate_with_(current_algorithm, optimal=False, run=True, config=config_path,
                   circles=30, all_curves=False, length=500, line_width=1.8,
                   title_size=20, label_size=16, color='#1E90FF')
