# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from caching.agent import Agent


agent = Agent.from_()
agent.initialize()
print agent.theta_hat_bk

second_agent = Agent.from_(cfg_file='myron.cfg')
second_agent.initialize()
print second_agent.theta_hat_bk
