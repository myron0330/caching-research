# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Display rewards
# **********************************************************************************#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict


AVAILABLE_MARKERS = ['o', '*', 's', '^', '<', '>']


def _standardize_(array, sigma=1.5):
    """
    Standardize array

    Args:
        array(list): standardize array
        sigma(int): sigma threshold
    """
    x_mean = np.mean(array)
    x_std = np.std(array)
    return map(lambda a: max(x_mean - sigma * x_std, min(x_mean + sigma * x_std, a)), array)


def display_single_(reward_data, all_curves=False, display_length=500, fig_size=(12, 8), line_width=1,
                    title_size=18, label_size=16, color='r', marker=None, marker_size=10,
                    title=u'回报对比图', x_label=u'迭代次数', y_label=u'回报收益', **kwargs):
    """
    Display single simulation rewards

    Args:
        reward_data(dict): dict of rewards
        all_curves(boolean): whether to display all reward curves
        display_length(int): length of plots
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        color(string): color of main curve
        marker(string): marker on point
        marker_size(float): marker size
        title(string): figure title
        x_label(string): x label string
        y_label(string): y label string
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
            plt.plot(frame[column][:display_length], linewidth=line_width, marker=marker, markersize=marker_size,
                     markerfacecolor='None',  markeredgewidth=line_width)
    else:
        plt.plot(frame['total'][:display_length], color=color, linewidth=line_width, marker=marker,
                 markersize=marker_size, markeredgecolor=color,
                 markerfacecolor='None',  markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center')
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top', horizontalalignment='center')
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90)
    plt.show()


def display_multiple_(rewards_data, display_length=500, fig_size=(12, 8), line_width=1,
                      title_size=18, label_size=16, marker=None, marker_size=10,
                      with_standardize=False, standardize_init=0,
                      title=u'回报对比图', x_label=u'迭代次数', y_label=u'回报收益', **kwargs):
    """
    Display multiple simulation rewards

    Args:
        rewards_data(dict): dict of dict of rewards
        display_length(int): length of plots
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        with_standardize(boolean): whether to do standardize
        standardize_init(int): standardize init value
        marker(string): marker on point
        marker_size(float): marker size
        title(string): figure title
        x_label(string): x label string
        y_label(string): y label string
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    max_y, min_y = 0, 1e10
    for _, reward in enumerate(rewards_data.values()):
        frame = pd.DataFrame(reward)
        frame['total'] = frame.sum(axis=1)
        max_y = max(max_y, frame['total'][:display_length].max())
        min_y = min(min_y, frame['total'][:display_length].min())
        current_marker = marker
        if marker == '':
            current_marker = AVAILABLE_MARKERS[_ % len(AVAILABLE_MARKERS)]
        curve = list(frame['total'][:display_length])
        if with_standardize:
            curve = curve[:standardize_init] + _standardize_(curve[standardize_init:])
        plt.plot(curve, color=DEFAULT_COLORS.get(_), linewidth=line_width,
                 marker=current_marker, markersize=marker_size, markerfacecolor='None',
                 markeredgecolor=DEFAULT_COLORS.get(_), markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k')
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top', horizontalalignment='center')
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90)
    legend = map(lambda x: x.upper(), rewards_data.keys())
    diff_y = max_y - min_y
    plt.ylim(min_y - diff_y * 0.05, max_y + diff_y * 0.05)
    plt.legend(legend, loc=4)
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
    rewards_90 = pickle.load(open('../performance/rewards.m-90.pk', 'r+'))
    rewards_70 = pickle.load(open('../performance/rewards.m-70.pk', 'r+'))
    rewards_50 = pickle.load(open('../performance/rewards.m-50.pk', 'r+'))
    rewards_30 = pickle.load(open('../performance/rewards.m-30.pk', 'r+'))
    rewards_20 = pickle.load(open('../performance/rewards.m-20.pk', 'r+'))
    rewards = OrderedDict(zip([20, 30, 50, 70, 90], [rewards_20, rewards_30, rewards_50, rewards_70, rewards_90]))
    display_multiple_(rewards, display_length=1000, line_width=1.8,
                      title_size=20, label_size=16, marker='', marker_size=3)
