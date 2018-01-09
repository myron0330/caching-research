# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: spider for video data
# **********************************************************************************#
import requests


url = 'https://www.youtube.com/channel/UCl8dMTqDrJQ0c8y23UBu4kQ'
data =requests.get(url)
print data
