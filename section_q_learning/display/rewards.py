# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Display rewards
# **********************************************************************************#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from collections import OrderedDict
from matplotlib import font_manager
from . base import standardize_


AVAILABLE_MARKERS = ['o', '*', 'p', 's', '^', '<', '>']
font_properties = font_manager.FontProperties()


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
                      title_size=18, label_size=16, marker=None, marker_size=10, legend_size=10,
                      with_standardize=False, standardize_init=0, sigma=1.5, standardize_special=True,
                      title='', x_label=u'迭代次数', y_label=u'回报收益',
                      save_path=None, x_axis=None, loc=None,
                      texts=None, with_q_values=False, alpha=0.8, **kwargs):
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
        standardize_special(boolean): standardize special
        sigma(int): sigma threshold
        marker(string): marker on point
        marker_size(float): marker size
        legend_size(float): legend_size
        title(string): figure title
        save_path(string): save path
        x_label(string): x label string
        y_label(string): y label string
        x_axis(list): x_axis
        loc(int): legend location
        with_q_values: with q values
        alpha: alpha parameters
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    max_y, min_y = 0, 1e10
    counter = 0 if len(rewards_data) == 4 else 1

    rewards_curve = OrderedDict()
    for _, reward in rewards_data.iteritems():
        if isinstance(reward[0], dict):
            frame = pd.DataFrame(reward)
            frame['total'] = frame.sum(axis=1)
            max_y = max(max_y, frame['total'][:display_length].max())
            min_y = min(min_y, frame['total'][:display_length].min())
            curve = list(frame['total'][:display_length])
        else:
            max_y = max([max_y] + reward)
            min_y = min([min_y] + reward)
            curve = reward
        if with_standardize:
            if standardize_special:
                if _ in ['CMAB']:
                    curve = curve[:standardize_init] + standardize_(curve[standardize_init:], sigma=sigma)
                elif _ in ['Q-learning']:
                    curve = curve[:5] + standardize_(curve[5:], sigma=sigma)
                else:
                    curve = standardize_(curve, sigma=sigma)
            else:
                curve = curve[:standardize_init] + standardize_(curve[standardize_init:], sigma=sigma)
        rewards_curve[_] = curve
    if 'B&B' in rewards_curve:
        rewards_curve['B&B'] = list(1.02 * np.max(np.array(rewards_curve.values()), axis=0))
        # rewards_curve['B&B'] = [380] * len(rewards_curve['B&B'])

    for _, curve in rewards_curve.iteritems():
        current_marker = marker
        if marker == '':
            current_marker = AVAILABLE_MARKERS[counter % len(AVAILABLE_MARKERS)]
        if x_axis is not None:
            plt.plot(x_axis, curve, color=DEFAULT_COLORS.get(counter), linewidth=line_width,
                     marker=current_marker, markersize=marker_size, markerfacecolor='None',
                     markeredgecolor=DEFAULT_COLORS.get(counter), markeredgewidth=line_width)
        else:
            plt.plot(curve, color=DEFAULT_COLORS.get(counter), linewidth=line_width,
                     marker=current_marker, markersize=marker_size, markerfacecolor='None',
                     markeredgecolor=DEFAULT_COLORS.get(counter), markeredgewidth=line_width)
        counter += 1
    if with_q_values and 'Q-learning' in rewards_curve:
        reward_list = rewards_curve['Q-learning']
        q_values = [0]
        for reward in reward_list:
            q_values.append(reward * alpha + (1 - alpha)*q_values[-1])
        q_values = q_values[1:]
        rewards_curve['Q-value'] = q_values
        plt.plot(q_values, '--k', linewidth=line_width,
                 marker='o', markersize=marker_size, markerfacecolor='None',
                 markeredgecolor='k', markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    # legend = map(lambda x: x.upper(), rewards_data.keys())
    legend = rewards_curve.keys()
    diff_y = max_y - min_y
    y_min_lim = kwargs.get('y_min_lim', min_y - diff_y * 0.05)
    y_max_lim = kwargs.get('y_max_lim', max_y + diff_y * 0.05)
    rcParams.update({'font.size': 14})
    plt.ylim(y_min_lim, y_max_lim)
    if x_axis:
        plt.xlim(x_axis[0], x_axis[-1])
    if loc is not None:
        plt.legend(legend, loc=loc, fontsize=legend_size)
    else:
        plt.legend(legend, loc='best', fontsize=legend_size)
    if texts is not None:
        for text in texts:
            plt.text(*text['args'], **text['kwargs'])
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()


DEFAULT_COLORS = {
    0: '#363636',
    1: '#FA8072',
    2: '#1E90FF',
    3: '#32CD32',
    4: '#FFD700',
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
