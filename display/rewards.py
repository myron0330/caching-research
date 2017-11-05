# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Display rewards
# **********************************************************************************#
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict


def display_single_(reward_data, all_curves=False, length=500, fig_size=(12, 8), line_width=1,
                    title_size=18, label_size=16, color='r', marker=None, marker_size=10):
    """
    Display single simulation rewards

    Args:
        reward_data(dict): dict of rewards
        all_curves(boolean): whether to display all reward curves
        length(int): length of plots
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        color(string): color of main curve
        marker(string): marker on point
        marker_size(float): marker size
    """
    frame = pd.DataFrame(reward_data)
    frame['total'] = frame.sum(axis=1)
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    if all_curves:
        for column in frame.columns:
            plt.plot(frame[column][:length], linewidth=line_width,  marker=marker, markersize=marker_size)
    else:
        plt.plot(frame['total'][:length], color=color, linewidth=line_width, marker=marker, markersize=marker_size)
    plt.title(u'算法-缓存回报对比图', fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center')
    plt.xlabel(u'迭代次数', fontsize=label_size, verticalalignment='top', horizontalalignment='center')
    plt.ylabel(u'回报收益', fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90)
    plt.show()


def display_multiple_(rewards_data, length=500, fig_size=(12, 8), line_width=1,
                      title_size=18, label_size=16, marker=None, marker_size=10):
    """
    Display multiple simulation rewards

    Args:
        rewards_data(OrderedDict): dict of dict of rewards
        length(int): length of plots
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        marker(string): marker on point
        marker_size(float): marker size
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    for _, reward in enumerate(rewards_data.values()):
        frame = pd.DataFrame(reward)
        frame['total'] = frame.sum(axis=1)
        plt.plot(frame['total'][:length], color=DEFAULT_COLORS.get(_), linewidth=line_width,
                 marker=marker, markersize=marker_size)
    plt.title(u'Memory-Reward对比图', fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k')
    plt.xlabel(u'迭代次数', fontsize=label_size, verticalalignment='top', horizontalalignment='center')
    plt.ylabel(u'回报收益', fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90)
    legend = ['Memory-{}'.format(_) for _ in rewards_data.keys()]
    plt.legend(legend, loc='best')
    plt.ylim(10, 65)
    plt.show()


DEFAULT_COLORS = {
    0: '#1E90FF',
    1: '#32CD32',
    2: '#FA8072',
    3: '#FFD700',
    4: '#363636'
}

if __name__ == '__main__':
    import pickle
    # display_single_(rewards, all_curves=False, length=1000, line_width=1.8, title_size=20,
    #                 label_size=16, color='#1E90FF', marker='*', marker_size=3)
    rewards_90 = pickle.load(open('../performance/rewards.m-90.pk', 'r+'))
    rewards_70 = pickle.load(open('../performance/rewards.m-70.pk', 'r+'))
    rewards_50 = pickle.load(open('../performance/rewards.m-50.pk', 'r+'))
    rewards_30 = pickle.load(open('../performance/rewards.m-30.pk', 'r+'))
    rewards_20 = pickle.load(open('../performance/rewards.m-20.pk', 'r+'))
    rewards = OrderedDict(zip([20, 30, 50, 70, 90], [rewards_20, rewards_30, rewards_50, rewards_70, rewards_90]))
    display_multiple_(rewards, length=1000, line_width=1.8,
                      title_size=20, label_size=16, marker='', marker_size=3)
