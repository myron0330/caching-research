# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#


class Algorithm(object):
    """
    Algorithm instance
    """
    def __init__(self, variables, theta_hat_bk, t_bk, c_bkt):
        self.variables = variables
        self.theta_hat_bk = theta_hat_bk
        self.t_bk = t_bk
        self.c_bkt = c_bkt

    def calculate_cbt(self):
        pass
