# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from section_cftl.agent import Agent


agent = Agent.from_()
agent.iter_with_('proposed_algorithm', circles=50, dump=False)
print agent.rewards
pass
