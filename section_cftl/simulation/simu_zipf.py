# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from collections import OrderedDict
from utils.random_utils import zipf_probabilities
from section_cftl.display.tools import display_dict_


data_dict = OrderedDict()
alphas = [0.9, 1.1, 1.3, 1.5][::-1]
for alpha in alphas:
    probabilities = zipf_probabilities(a=alpha, low_bound=0, up_bound=50)
    cumulative_probabilities = [0]
    for item in probabilities:
        cumulative_probabilities.append(cumulative_probabilities[-1]+item)
    data_dict['$\\gamma = {}$'.format(alpha)] = cumulative_probabilities
print data_dict


parameters = {
    'counter': 0,
    'display_length': 1000,
    'line_width': 2.5,
    'title_size': 20,
    'label_size': 16,
    'marker': '',
    'marker_size': 8,
    'title': '',
    'x_label': u'',
    'y_label': u'',
    'with_standardize': False,
    'standardize_init': 0,
    'sigma': 1.5,
    'loc': 4,
    'legend_size': 15,
    'y_min_lim': 0,
    'y_max_lim': 1,
    'texts': [
        {
            'args': (25, -0.08, 'File ranking'),
            'kwargs': {
                'horizontalalignment': 'center',
                'verticalalignment': 'center',
                'fontsize': 18,
            }
        },
        {
            'args': (-3, 0.5, 'CDF of zipf distribution'),
            'kwargs': {
                'horizontalalignment': 'center',
                'verticalalignment': 'center',
                'fontsize': 18,
                'rotation': 90,
            }
        }
    ],
    'save_path': '../plots/zipf.jpg',
}
display_dict_(data_dict, **parameters)
