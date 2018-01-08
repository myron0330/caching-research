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
        :param item:
        :return:
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


__all__ = [
    'CategorySchema'
]