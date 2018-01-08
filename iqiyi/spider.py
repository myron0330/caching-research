# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import requests
from mongo_api import update_one_, query_from_
from schema import CategorySchema


class Spider(object):

    def __init__(self, urls, collections):
        self.urls = urls
        self.collections = collections

    def scramble_category_info(self):
        """
        Scramble category info
        """
        category_url = self.urls.category_url
        data = requests.get(category_url).json()['data']
        for item in data:
            update_one_(self.collections.category, CategorySchema.from_requests(item))

    def query_(self, collection, key=None, **kwargs):
        """
        Query collections from mongodb
        """
        if isinstance(collection, (str, unicode)):
            collection = getattr(self.collections, collection)
        return query_from_(collection, key=key, **kwargs)


if __name__ == '__main__':
    from urls import Urls
    from mongo_base import Collections
    spider = Spider(urls=Urls, collections=Collections)
    print spider.query_('category', key='category_id')
