# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from section_cmab.variables import Variables

variable = Variables.from_('default.cfg')
print variable.base_stations
print variable.to_dict()
