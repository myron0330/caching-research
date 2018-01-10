# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
import requests
from urls import Urls
from mongo_base import Collections, BatchOps
from mongo_api import update_one_, query_from_, dump_to_
from schema import CategorySchema, AlbumSchema, VideoSchema


def _query_category_ids():
    """
    Query category ids
    """
    category_ids = map(lambda x: x['category_id'], query_from_(Collections.category, fields={'category_id': 1}))
    return category_ids


def _query_play_urls():
    """
    Query play urls
    """
    play_urls = map(lambda x: x['play_url'], query_from_(Collections.album, fields={'play_url': 1}))
    return play_urls


def _get_total_page(total_size, page_size):
    """
    Get total page
    """
    quotient, remainder = total_size / page_size, total_size % page_size
    total_page = quotient + min(1, remainder)
    return total_page


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

    def scramble_album_info(self, category_ids=None, with_all_pages=True, start_count=0):
        """
        Scramble album info

        Args:
            category_ids(list): category ids
            with_all_pages(boolean): whether to scramble all pages.
            start_count(int): start count
        """
        category_ids = category_ids or _query_category_ids()
        total_count = 0
        exception_count = 0
        for category_id in category_ids:
            page_id = 1
            first_page = self._request_album_info_by(category_id=category_id, page_id=page_id)
            first_page_schema = map(AlbumSchema.from_requests, first_page['data'])
            dump_to_(BatchOps.album, first_page_schema)
            total_count += 1
            print '[ALBUM] category_id: {}, page_id: {}, ' \
                  'total_count: {}, exception_count: {}, page_count: {}'.format(category_id, page_id,
                                                                                total_count,
                                                                                exception_count,
                                                                                len(first_page_schema))
            if not with_all_pages:
                continue
            total, page_size = first_page['total'], first_page['pagesize']
            total_page = _get_total_page(total_size=total, page_size=page_size)
            for page_id in xrange(2, total_page):
                if total_count >= start_count:
                    try:
                        page = self._request_album_info_by(category_id=category_id, page_id=page_id)
                        page_schema = map(AlbumSchema.from_requests, page['data'])
                        dump_to_(BatchOps.album, page_schema)
                        page_count = len(page_schema)
                    except:
                        exception_count += 1
                        page_count = 0
                total_count += 1
                print '[ALBUM] category_id: {}, page_id: {}, ' \
                      'total_count: {}, exception_count: {}, page_count: {}'.format(category_id, page_id,
                                                                                    total_count, exception_count,
                                                                                    page_count)

    def scramble_video_info(self, play_urls=None, start_count=0):
        """
        Scramble video info

        Args:
            play_urls(list): play urls
            start_count(int): start count
        """
        play_urls = play_urls or _query_play_urls()
        total_count = 0
        exception_count = 0
        for play_url in play_urls:
            if total_count >= start_count:
                try:
                    video = self._request_video_info_by(play_url)['data']
                    video_schema = VideoSchema.from_requests(video)
                    dump_to_(BatchOps.video, video_schema)
                except:
                    exception_count += 1
            total_count += 1
            print '[Video] play_url: {}, total_count: {}, exception_count: {}'.format(play_url,
                                                                                      total_count,
                                                                                      exception_count)

    @staticmethod
    def _request_album_info_by(category_id=None, page_id=1):
        """
        Scramble album info
        """
        album_url = Urls.album_url.format(category_id=category_id, page_id=page_id)
        data = requests.get(album_url).json()
        return data

    @staticmethod
    def _request_video_info_by(play_url=None):
        """
        Scramble video info
        """
        album_url = Urls.video_url.format(play_url=play_url)
        data = requests.get(album_url).json()
        return data


if __name__ == '__main__':
    spider = Spider()
    # spider.scramble_category_info()
    # print spider.query_('category', key='category_id')
    # spider.scramble_album_info(category_ids=[1], with_all_pages=False)
    # print spider.scramble_video_info(play_urls=['http://www.iqiyi.com/v_19rreslrhw.html?vfm=newvfm'])
    spider.scramble_album_info(start_count=0)
    spider.scramble_video_info()
