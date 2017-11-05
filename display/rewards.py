# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Display rewards
# **********************************************************************************#
import pandas as pd
import matplotlib.pyplot as plt


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
    plt.title(u'缓存算法迭代-回报收益图', fontsize=title_size, verticalalignment='bottom',
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
        rewards_data(list): list of dict of rewards
        length(int): length of plots
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        color(string): color of main curve
        marker(string): marker on point
        marker_size(float): marker size
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    for reward in rewards_data:
        frame = pd.DataFrame(reward)
        frame['total'] = frame.sum(axis=1)
        plt.plot(frame['total'][:length], linewidth=line_width, marker=marker, markersize=marker_size)
    plt.title(u'缓存算法迭代-回报收益图', fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center')
    plt.xlabel(u'迭代次数', fontsize=label_size, verticalalignment='top', horizontalalignment='center')
    plt.ylabel(u'回报收益', fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90)
    plt.show()


if __name__ == '__main__':
    import pickle
    rewards = pickle.load(open('../performance/rewards.memory-50.pk', 'r+'))
    # display_single_(rewards, all_curves=False, length=1000, line_width=1.8, title_size=20,
    #                 label_size=16, color='#1E90FF', marker='*', marker_size=3)
    rewards_30 = pickle.load(open('../performance/rewards.memory-30.pk', 'r+'))
    rewards_20 = pickle.load(open('../performance/rewards.memory-20.pk', 'r+'))

    display_multiple_([rewards, rewards_30, rewards_20], length=1000, line_width=1.8, title_size=20,
                      label_size=16, marker='*', marker_size=3)
