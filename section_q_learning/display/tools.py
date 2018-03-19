# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
from . base import standardize_, moving_average_


AVAILABLE_MARKERS = ['o', '*', 'p', 's', '^', '<', '>']
font_properties = font_manager.FontProperties()

DEFAULT_COLORS = {
    0: '#363636',
    1: '#FA8072',
    2: '#1E90FF',
    3: '#32CD32',
    4: '#FFD700',
    5: '#7CFC00',
    6: '#EE6363',
    7: '#009ACD',
}


def display_dict_(data, fig_size=(12, 8), line_width=1,
                  title_size=18, label_size=16, marker=None,
                  marker_size=10, legend_size=10,
                  title='', x_label=u'迭代次数', y_label=u'回报收益',
                  save_path=None, x_axis=None, loc=None,
                  with_standardize=False, standardize_init=0, sigma=1.5,
                  texts=None, counter=0, with_legend=True,
                  with_ma=False, ma_periods=3, with_variation=False,  **kwargs):
    """
    Display multiple simulation rewards

    Args:
        data(dict): dict of list
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        marker(string): marker on point
        marker_size(float): marker size
        legend_size(float): legend_size
        title(string): figure title
        save_path(string): save path
        x_label(string): x label string
        y_label(string): y label string
        with_standardize(boolean): whether to do standardize
        standardize_init(int): standardize init value
        sigma(int): sigma threshold
        x_axis(list): x_axis
        loc(int): legend location
        counter(int): counter for marker
        with_legend(boolean): with legend
        with_ma(boolean): with moving average
        ma_periods(int): ma periods
        with_variation(boolean): with variation
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    max_y, min_y = 0, 1e10

    curves = list()
    for _, curve in data.iteritems():
        if with_ma:
            curve = moving_average_(curve, ma_periods)
        if with_standardize:
            curve = curve[:standardize_init] + standardize_(curve[standardize_init:], sigma=sigma)
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
        curves.append(curve)
        counter += 1
    if with_variation:
        matrix = np.matrix(curves)
        variation = matrix.var(axis=0).tolist()[0]
        if x_axis is not None:
            plt.plot(x_axis, variation, '--r', linewidth=line_width, marker='^', markersize=marker_size,
                     markeredgecolor='r', markeredgewidth=line_width)
        else:
            plt.plot(variation, '--r', linewidth=line_width, marker='*', markersize=marker_size,
                     markeredgecolor='r', markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    legend = data.keys()
    diff_y = max_y - min_y
    y_min_lim = kwargs.get('y_min_lim', min_y - diff_y * 0.05)
    y_max_lim = kwargs.get('y_max_lim', max_y + diff_y * 0.05)
    rcParams.update({'font.size': 14})
    plt.ylim(y_min_lim, y_max_lim)
    if x_axis:
        plt.xlim(x_axis[0], x_axis[-1])
    if with_legend:
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


def display_list_(data, fig_size=(12, 8), line_width=1,
                  title_size=18, label_size=16, marker=None,
                  marker_size=10, legend_size=10,
                  title='', x_label=u'迭代次数', y_label=u'回报收益',
                  save_path=None, x_axis=None, loc=None,
                  with_standardize=False, standardize_init=0, sigma=1.5,
                  texts=None, color=None, display_length=None,  **kwargs):
    """
    Display multiple simulation rewards

    Args:
        data(list): list
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        marker(string): marker on point
        marker_size(float): marker size
        legend_size(float): legend_size
        title(string): figure title
        save_path(string): save path
        x_label(string): x label string
        y_label(string): y label string
        with_standardize(boolean): whether to do standardize
        standardize_init(int): standardize init value
        sigma(int): sigma threshold
        x_axis(list): x_axis
        loc(int): legend location
        display_length(int): display length
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    max_y, min_y = 0, 1e10
    curve = data
    if with_standardize:
        curve = curve[:standardize_init] + standardize_(curve[standardize_init:], sigma=sigma)
    if display_length:
        curve = curve[:display_length]
    if x_axis is not None:
        plt.plot(x_axis, curve, color=color, linewidth=line_width,
                 marker=marker, markersize=marker_size, markerfacecolor='None',
                 markeredgecolor=color, markeredgewidth=line_width)
    else:
        plt.plot(curve, color=color, linewidth=line_width,
                 marker=marker, markersize=marker_size, markerfacecolor='None',
                 markeredgecolor=color, markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    diff_y = max_y - min_y
    y_min_lim = kwargs.get('y_min_lim', min_y - diff_y * 0.05)
    y_max_lim = kwargs.get('y_max_lim', max_y + diff_y * 0.05)
    rcParams.update({'font.size': 14})
    plt.ylim(y_min_lim, y_max_lim)
    if x_axis:
        plt.xlim(x_axis[0], x_axis[-1])
    if texts is not None:
        for text in texts:
            plt.text(*text['args'], **text['kwargs'])
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()


def display_distributed_(data, fig_size=(12, 8), line_width=1,
                         title_size=18, label_size=16, marker=None,
                         marker_size=10, legend_size=10,
                         title='', x_label=u'迭代次数', y_label=u'回报收益',
                         save_path=None, x_axis=None, loc=None,
                         with_standardize=False, standardize_init=0, sigma=1.5,
                         texts=None, counter=0, with_legend=True,
                         with_ma=False, ma_periods=3, with_variation=False,  **kwargs):
    """
    Display multiple simulation rewards

    Args:
        data(dict): dict of list
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        marker(string): marker on point
        marker_size(float): marker size
        legend_size(float): legend_size
        title(string): figure title
        save_path(string): save path
        x_label(string): x label string
        y_label(string): y label string
        with_standardize(boolean): whether to do standardize
        standardize_init(int): standardize init value
        sigma(int): sigma threshold
        x_axis(list): x_axis
        loc(int): legend location
        counter(int): counter for marker
        with_legend(boolean): with legend
        with_ma(boolean): with moving average
        ma_periods(int): ma periods
        with_variation(boolean): with variation
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')

    max_y, min_y = 0, 1e10
    right_axis = ax.twinx()

    curves = list()
    for _, curve in data.iteritems():
        if with_ma:
            curve = moving_average_(curve, ma_periods)
        if with_standardize:
            curve = curve[:standardize_init] + standardize_(curve[standardize_init:], sigma=sigma)
        current_marker = marker
        if marker == '':
            current_marker = AVAILABLE_MARKERS[counter % len(AVAILABLE_MARKERS)]
        if x_axis is not None:
            ax.plot(x_axis, curve, linewidth=line_width,
                    marker=current_marker, markersize=marker_size,
                    markerfacecolor='None',
                    markeredgewidth=line_width)
            # ax.plot(x_axis, curve, color=DEFAULT_COLORS.get(counter), linewidth=line_width,
            #         marker=current_marker, markersize=marker_size, markerfacecolor='None',
            #         markeredgecolor=DEFAULT_COLORS.get(counter), markeredgewidth=line_width)
        else:
            ax.plot(curve, linewidth=line_width, marker=current_marker,
                    markersize=marker_size, markerfacecolor='None',
                    markeredgewidth=line_width)
            # ax.plot(curve, color=DEFAULT_COLORS.get(counter), linewidth=line_width,
            #         marker=current_marker, markersize=marker_size, markerfacecolor='None',
            #         markeredgecolor=DEFAULT_COLORS.get(counter), markeredgewidth=line_width)
        curves.append(curve)
        counter += 1
    if with_variation:
        matrix = np.matrix(curves)
        variation = matrix.var(axis=0).tolist()[0]
        right_axis.plot(variation, '--k', linewidth=2*line_width, marker='>', markersize=marker_size,
                        markeredgecolor='k', markeredgewidth=2*line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    legend = data.keys()
    diff_y = max_y - min_y
    y_min_lim = kwargs.get('y_min_lim', min_y - diff_y * 0.05)
    y_max_lim = kwargs.get('y_max_lim', max_y + diff_y * 0.05)
    rcParams.update({'font.size': 14})
    ax.set_ylim(y_min_lim, y_max_lim)
    if x_axis:
        plt.xlim(x_axis[0], x_axis[-1])
    if with_legend:
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
