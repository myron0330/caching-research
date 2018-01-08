# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
database = client['iqiyi']
category_collection = database['category']


class Collections(object):

    category = category_collection
