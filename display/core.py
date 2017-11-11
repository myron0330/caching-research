# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import pickle
from collections import OrderedDict
from rewards import display_multiple_, display_single_


def draw_memory_comparison_plot():
    """
    Display memory comparison figures
    """
    rewards_90 = pickle.load(open('../performance/rewards.m-90.pk', 'r+'))
    rewards_70 = pickle.load(open('../performance/rewards.m-70.pk', 'r+'))
    rewards_50 = pickle.load(open('../performance/rewards.m-50.pk', 'r+'))
    rewards_30 = pickle.load(open('../performance/rewards.m-30.pk', 'r+'))
    rewards_20 = pickle.load(open('../performance/rewards.m-20.pk', 'r+'))
    rewards = OrderedDict(zip([20, 30, 50, 70, 90], [rewards_20, rewards_30, rewards_50, rewards_70, rewards_90]))
    display_multiple_(rewards, display_length=1000, line_width=1.8, title_size=20, label_size=16, marker='', marker_size=3)


def draw_algorithm_plot():
    """
    Display algorithm comparison figures
    """
    rewards_50 = pickle.load(open('../performance/rewards.pk', 'r+'))
    display_single_(rewards_50, all_curves=False, length=40, line_width=2, title_size=20,
                    label_size=16, color='#1E90FF', marker='p', marker_size=8)


def draw_algorithm_comparison_plot(performance_files=list()):
    """
    Display memory comparison figures
    """
    rewards_keys = map(lambda x: x.split('.')[1][2:], performance_files)
    rewards_values = map(lambda x: pickle.load(open('../performance/{}'.format(x), 'r+')), performance_files)
    rewards = OrderedDict(zip(rewards_keys, rewards_values))
    display_multiple_(rewards, display_length=30, line_width=2, title_size=20, label_size=16, marker='*', marker_size=5)


if __name__ == '__main__':
    # draw_memory_comparison_plot()
    # draw_algorithm_plot()
    draw_algorithm_comparison_plot(['rewards.a-branch_and_bound.m-15.pk', 'rewards.a-primal_dual_recover.m-15.pk'])
