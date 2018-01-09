# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: iqiyi url
# **********************************************************************************#


def with_parameter_(url, authenticate=True, **params):
    """
    Add parameters to url

    Args:
        url(string): url
        authenticate(boolean): whether to authenticate
        params(dict): parameters
    """
    params_args = '&'.join(['{}={}'.format(key, value) for key, value in params.iteritems()])
    url = '?'.join([url, params_args]) if params_args else url
    if authenticate:
        linker = '&' if '?' in url else '?'
        token_args = 'apiKey=71c300df4a7f4e89a43d8e19e5458e6f'
        url = linker.join([url, token_args])
    return url


class Urls(object):

    category_url = with_parameter_('http://expand.video.iqiyi.com/api/category/list.json')
    album_url = with_parameter_('http://expand.video.iqiyi.com/api/album/list.json?'
                                'categoryId={category_id}&pageId={page_id}')
