# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
from __future__ import division
import numpy as np
from copy import copy
from collections import OrderedDict
from section_cftl.agent import Agent
from utils.random_utils import zipf_array, random_choose_
from section_cftl.display.tools import display_dict_


def sample_(matrix, target_fields, reshape_size=None):
    matrix = copy(matrix)
    matrix = matrix.reshape((1, matrix.size))
    multiplier = np.zeros(matrix.size)
    for _ in xrange(len(multiplier)):
        if _+1 in target_fields:
            multiplier[_] = 1
    matrix *= multiplier
    if reshape_size:
        matrix = matrix.reshape(reshape_size)
    return matrix


agent = Agent.from_()
target_domain = np.zeros((agent.variables.user_number, agent.variables.file_number))
for node in agent.users_network.nodes_info:
    array = zipf_array(a=agent.variables.zipf_a, low_bound=0,
                       up_bound=len(agent.variables.files),
                       size=1000,
                       seed=node * 1000)
    array_length = len(array)
    probabilities = list()
    for _ in agent.variables.files:
        probabilities.append(array.count(_ + 1) / array_length)
    target_domain[node, :] = probabilities


percents = [0.02, 0.04, 0.06, 0.08, 0.1]
for percent in percents:
    target_valid_fields = random_choose_(percent=percent,
                                         lower_bound=0,
                                         upper_bound=target_domain.size-1,
                                         matrix_size=target_domain.size,
                                         seed=0)
    sampled_target_domain = sample_(target_domain, target_valid_fields,
                                    reshape_size=(agent.variables.user_number, agent.variables.file_number))
    diff_target = target_domain - sampled_target_domain
    a, b, c = np.linalg.svd(sampled_target_domain, full_matrices=False)
    estimated_target_domain = np.dot(a * b, c)
    print percent
    print (estimated_target_domain - sampled_target_domain).std()
    print (estimated_target_domain - target_domain).std()
    print '\n'

percents = [0.02, 0.04, 0.06, 0.08, 0.1]
with_tl = [0.012, 0.008, 0.0059, 0.0045, 0.0042]
without_tl = [0.0202, 0.0143, 0.0109, 0.0095, 0.0088]
parameters = {
    'counter': 1,
    'display_length': 1000,
    'line_width': 3,
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
    'loc': 'best',
    'legend_size': 15,
    'y_min_lim': 0.,
    'y_max_lim': 0.025,
    'x_axis': map(lambda x: x * 100, percents),
    'x_min_lim': 2,
    'x_max_lim': 10,
    'texts': [
        {
            'args': (6, -0.002, 'Sparsity (%)'),
            'kwargs': {
                'horizontalalignment': 'center',
                'verticalalignment': 'center',
                'fontsize': 18,
            }
        },
        {
            'args': (1.25, 0.0125, 'RMSE'),
            'kwargs': {
                'horizontalalignment': 'center',
                'verticalalignment': 'center',
                'fontsize': 18,
                'rotation': 90,
            }
        }
    ],
    'save_path': '../plots/tl.jpg',
}
data = OrderedDict()
data['with Transfer Learning'] = with_tl
data['without Transfer Learning'] = without_tl
display_dict_(data, **parameters)
