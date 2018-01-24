# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Display rewards
# **********************************************************************************#
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager


AVAILABLE_MARKERS = ['o', '*', 'p', 's', '^', '<', '>']
font_properties = font_manager.FontProperties()


def display_latency(latency_data, display_length=500, fig_size=(12, 8), line_width=1,
                    title_size=18, label_size=16, marker=None, marker_size=10, legend_size=10,
                    title='', x_label=u'迭代次数', y_label=u'回报收益',
                    save_path=None, x_axis=None, loc=None,
                    texts=None, **kwargs):
    """
    Display multiple simulation rewards

    Args:
        latency_data(dict): dict of latency data
        display_length(int): length of plots
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
        x_axis(list): x_axis
        loc(int): legend location
        texts(list): list of text
    """
    fig = plt.figure(figsize=fig_size)
    axes = fig.add_subplot(1, 1, 1)
    axes.spines['left'].set_color('black')
    axes.spines['right'].set_color('black')
    axes.spines['top'].set_color('black')
    axes.spines['bottom'].set_color('black')
    max_y, min_y = 0, 1e10
    counter = 0 if len(latency_data) == 4 else 1
    for _, latency in latency_data.iteritems():
        curve = latency[:display_length]
        min_y = min(min_y, min(curve))
        max_y = max(max_y, max(curve))
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
    plt.title(title, fontsize=title_size, verticalalignment='bottom',
              horizontalalignment='center', color='k', fontproperties=font_properties)
    font_properties.set_size(label_size)
    plt.xlabel(x_label, fontsize=label_size, verticalalignment='top',
               horizontalalignment='center', fontproperties=font_properties)
    plt.ylabel(y_label, fontsize=label_size, verticalalignment='bottom',
               horizontalalignment='center', rotation=90,  fontproperties=font_properties)
    legend = latency_data.keys()
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
    pass

