# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import requests
from urls import Urls
from mongo_base import Collections
from mongo_api import update_one_, query_from_
from schema import CategorySchema


def _query_category_ids():
    """
    Query category ids
    """
    category_ids = map(lambda x: x['category_id'], query_from_(Collections.category, fields={'category_id': 1}))
    return category_ids


class Spider(object):

    @staticmethod
    def scramble_category_info():
        """
        Scramble category info
        """
        category_url = Urls.category_url
        data = requests.get(category_url).json()['data']
        for item in data:
            update_one_(Collections.category, CategorySchema.from_requests(item))

    def scramble_album_info(self):
        """
        Scramble album info
        """
        category_ids = _query_category_ids()
        for category_id in category_ids:
            page_id = 1
            first_page = self._request_album_info_by(category_id=category_id, page_id=page_id)
            total, page_size = first_page['total'], first_page['pagesize']

            pass

    @staticmethod
    def _request_album_info_by(category_id=None, page_id=1):
        """
        Scramble album info
        """
        album_url = Urls.album_url.format(category_id=category_id, page_id=page_id)
        data = requests.get(album_url).json()
        return data


if __name__ == '__main__':
    spider = Spider()
    # spider.scramble_category_info()
    # print spider.query_('category', key='category_id')
    spider.scramble_album_info()
