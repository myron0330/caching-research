# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
from matplotlib.ticker import FormatStrFormatter


DEFAULT_COLORS = {
    0: '#363636',
    1: '#FA8072',
    2: '#1E90FF',
    3: '#32CD32',
    4: '#FFD700',
}
AVAILABLE_MARKERS = ['o', '*', 'p', 's', '^', '<', '>']
font_properties = font_manager.FontProperties()


def display_rewards_(fig_size=(11, 8), line_width=1,
                     title_size=18, label_size=16, marker_size=10, legend_size=10,
                     title='', x_label=u'迭代次数', y_label=u'回报收益',
                     save_path=None, x_axis=None, loc=None,
                     texts=None, **kwargs):
    """
    Display multiple simulation rewards

    Args:
        fig_size(tuple): figure size
        line_width(float): line width
        title_size(float): title size
        label_size(float): label size
        marker_size(float): marker size
        legend_size(float): legend_size
        title(string): figure title
        save_path(string): save path
        x_label(string): x label string
        y_label(string): y label string
        x_axis(list): x_axis
        loc(int): legend location
    """
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    x_axis = range(0, 10)
    y_axis = range(0, 10)[::-1]
    current_marker = AVAILABLE_MARKERS[0]
    current_color = DEFAULT_COLORS.get(2)
    plt.plot(x_axis, y_axis, color=current_color, linewidth=line_width,
             marker=current_marker, markersize=marker_size, markerfacecolor='None',
             markeredgecolor=current_color, markeredgewidth=line_width)
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    legend = ['reward-latency']
    rcParams.update({'font.size': 14})
    xmajorFormatter = FormatStrFormatter('')
    ymajorFormatter = FormatStrFormatter('')
    ax.xaxis.set_major_formatter(xmajorFormatter)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.plot([0, 4.5], [4.5]*2, '--k', linewidth=line_width)
    plt.plot([4.5]*2, [0, 4.5], '--k', linewidth=line_width)

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


if __name__ == '__main__':
    parameters = {
        'display_length': 50,
        'line_width': 2.5,
        'title_size': 20,
        'label_size': 16,
        'marker': '',
        'marker_size': 8,
        'title': '',
        'x_label': u'',
        'y_label': u'',
        'all_curves': True,
        'with_standardize': True,
        'standardize_init': 25,
        'sigma': 0.6,
        'loc': '3',
        'legend_size': 15,
        'fixed_theta': True,
        'y_min_lim': 0,
        'texts': [
            {
                'args': (9, -0.3, '$\Delta T$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 14,
                }
            },
            {
                'args': (-0.6, 9, '$d_{b,k,t}\Delta TR_{0}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 14,
                    'rotation': 0,
                }
            },
            {
                'args': (4.5, -0.4, '$l_{b,k,t}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                }
            },
            {
                'args': (-0.5, 4.5, '$r_{b,k,t}$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 20,
                    'rotation': 0,
                }
            },
            {
                'args': (-0.3, -0.3, '$0$'),
                'kwargs': {
                    'horizontalalignment': 'center',
                    'verticalalignment': 'center',
                    'fontsize': 14,
                    'rotation': 0,
                }
            }
        ],
        'save_path': '../plots/latency_vs_rewards.jpg',
    }
    display_rewards_(**parameters)
