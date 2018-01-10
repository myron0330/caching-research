# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from core.objects import ValueObject


class CategorySchema(ValueObject):

    __slots__ = [
        'category_id',
        'short_name',
        'category_name'
    ]

    def __init__(self, category_id=None, short_name=None, category_name=None):
        self.category_id = category_id
        self.short_name = short_name
        self.category_name = category_name

    @classmethod
    def from_requests(cls, item):
        """
        requests from iqiyi
        """
        item['category_id'] = item.pop('categoryId')
        item['short_name'] = item.pop('shortName')
        item['category_name'] = item.pop('categoryName')
        return cls(**item)

    @classmethod
    def from_query(cls, item):
        """
        query from mongodb
        """
        return cls(**item)

    def to_mongodb_item(self):
        """
        To mongodb item
        """
        return (
            {
                'category_id': self.category_id,
            },
            {
                '$set': {
                    'short_name': self.short_name,
                    'category_name': self.category_name
                }
            }
        )


class AlbumSchema(ValueObject):

    __slots__ = [
        'actor',
        'album_id',
        'album_name',
        'album_status',
        'album_type',
        'album_url',
        'area',
        'category_id',
        'created_time',
        'desc',
        'director',
        'html5_play_url',
        'html5_url',
        'is_3d',
        'is_purchase',
        'keyword',
        'play_url',
        'purchase_type',
        'score',
        'source_id',
        'qi_pu_id',
        'source_qi_pu_id'
    ]

    def __init__(self, actor=None, album_id=None, album_name=None,
                 album_status=None, album_type=None, album_url=None,
                 area=None, category_id=None, created_time=None,
                 desc=None, director=None, html5_play_url=None,
                 html5_url=None, is_3d=None, is_purchase=None,
                 keyword=None, play_url=None, purchase_type=None,
                 score=None, source_id=None, qi_pu_id=None,
                 source_qi_pu_id=None, **kwargs):
        self.actor = actor
        self.album_id = album_id
        self.album_name = album_name
        self.album_status = album_status
        self.album_type = album_type
        self.album_url = album_url
        self.area = area
        self.category_id = category_id
        self.created_time = created_time
        self.desc = desc
        self.director = director
        self.html5_play_url = html5_play_url
        self.html5_url = html5_url
        self.is_3d = is_3d
        self.is_purchase = is_purchase
        self.keyword = keyword
        self.play_url = play_url
        self.purchase_type = purchase_type
        self.score = score
        self.source_id = source_id
        self.qi_pu_id = qi_pu_id
        self.source_qi_pu_id = source_qi_pu_id

    @classmethod
    def from_requests(cls, item):
        return cls(
            actor=item['actor'],
            album_id=item['albumId'],
            album_name=item['albumName'],
            album_status=item['albumStatus'],
            album_type=item['albumType'],
            album_url=item['albumUrl'],
            area=item['area'],
            category_id=item['categoryId'],
            created_time=item['createdTime'],
            desc=item['desc'],
            director=item['director'],
            html5_play_url=item['html5PlayUrl'],
            html5_url=item['html5Url'],
            is_3d=item['is3D'],
            is_purchase=item['isPurchase'],
            keyword=item['keyword'],
            play_url=item['playUrl'],
            purchase_type=item['purchaseType'],
            score=item['score'],
            source_id=item['sourceId'],
            qi_pu_id=item['qipuId'],
            source_qi_pu_id=item['sourceQipuId']
        )

    @classmethod
    def from_query(cls, item):
        """
        query from mongodb
        """
        return cls(**item)

    def to_mongodb_item(self):
        """
        To mongodb item
        """
        return (
            {
                'album_id': self.album_id,
            },
            {
                '$set': {
                    'actor': self.actor,
                    'album_id': self.album_id,
                    'album_name': self.album_name,
                    'album_status': self.album_status,
                    'album_type': self.album_type,
                    'album_url': self.album_url,
                    'area': self.area,
                    'category_id': self.category_id,
                    'created_time': self.created_time,
                    'desc': self.desc,
                    'director': self.director,
                    'html5_play_url': self.html5_play_url,
                    'html5_url': self.html5_url,
                    'is_3d': self.is_3d,
                    'is_purchase': self.is_purchase,
                    'keyword': self.keyword,
                    'play_url': self.play_url,
                    'purchase_type': self.purchase_type,
                    'score': self.score,
                    'source_id': self.source_id,
                    'qi_pu_id': self.qi_pu_id,
                    'source_qi_pu_id': self.source_qi_pu_id
                }
            }
        )


class VideoSchema(ValueObject):

    __slots__ = [
        'album',
        'album_qi_pu_id',
        'update_time',
        'copyright_id',
        'tv_id',
        'vid',
        'title',
        'url',
        'play_num',
        'main_actors',
        'category_id',
        'site',
        'related_streams',
        'swf',
        'album_id',
        'stream_type',
        'tag',
        'qi_pu_id',
        'duration',
        'img_url',
    ]

    def __init__(self, album=None, album_qi_pu_id=None, update_time=None,
                 copyright_id=None, tv_id=None, vid=None, title=None,
                 url=None, play_num=None, main_actors=None,
                 category_id=None, site=None, related_streams=None,
                 swf=None, album_id=None, stream_type=None,
                 tag=None, qi_pu_id=None, duration=None, img_url=None, **kwargs):
        self.album = album
        self.album_qi_pu_id = album_qi_pu_id
        self.update_time = update_time
        self.copyright_id = copyright_id
        self.tv_id = tv_id
        self.vid = vid
        self.title = title
        self.url = url
        self.play_num = play_num
        self.main_actors = main_actors
        self.category_id = category_id
        self.site = site
        self.related_streams = related_streams
        self.swf = swf
        self.album_id = album_id
        self.stream_type = stream_type
        self.tag = tag
        self.qi_pu_id = qi_pu_id
        self.duration = duration
        self.img_url = img_url

    @classmethod
    def from_requests(cls, item):
        return cls(
            album=item['album'],
            album_qi_pu_id=item['albumQipuId'],
            update_time=item['updateTime'],
            copyright_id=item['copyrightId'],
            tv_id=item['tvId'],
            vid=item['vid'],
            title=item['title'],
            url=item['url'],
            play_num=item['playNum'],
            main_actors=item['mainActors'],
            category_id=item['categoryId'],
            site=item['site'],
            related_streams=item['relatedStreams'],
            swf=item['swf'],
            album_id=item['albumId'],
            stream_type=item['streamType'],
            tag=item['tag'],
            qi_pu_id=item['qipuId'],
            duration=item['duration'],
            img_url=item['imghUrl']
        )

    @classmethod
    def from_query(cls, item):
        """
        query from mongodb
        """
        return cls(**item)

    def to_mongodb_item(self):
        """
        To mongodb item
        """
        return (
            {
                'qi_pu_id': self.qi_pu_id,
            },
            {
                '$set': {
                    'album': self.album,
                    'album_qi_pu_id': self.album_qi_pu_id,
                    'update_time': self.update_time,
                    'copyright_id': self.copyright_id,
                    'tv_id': self.tv_id,
                    'vid': self.vid,
                    'title': self.title,
                    'url': self.url,
                    'play_num': self.play_num,
                    'main_actors': self.main_actors,
                    'category_id': self.category_id,
                    'site': self.site,
                    'related_streams': self.related_streams,
                    'swf': self.swf,
                    'album_id': self.album_id,
                    'stream_type': self.stream_type,
                    'tag': self.tag,
                    'qi_pu_id': self.qi_pu_id,
                    'duration': self.duration,
                    'img_url': self.img_url
                }
            }
        )


__all__ = [
    'CategorySchema',
    'AlbumSchema'
]
