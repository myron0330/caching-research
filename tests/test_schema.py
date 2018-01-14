# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from iqiyi.mongo_base import Collections
from iqiyi.mongo_api import query_from_


data = query_from_(Collections.album, key=None, fields={'play_url': 1})
pass
