# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from mongo_base import Collections
from schema import *


def update_one_(collection, schema):
    """
    Update one schema
    """
    query_field, item = schema.to_mongodb_item()
    collection.update_one(query_field, item, upsert=True)


def query_from_(collection, key=None, **kwargs):
    """
    Query from schemas from collection
    """
    if collection == Collections.category:
        schema = CategorySchema
    else:
        raise Exception('Schema Error')
    items = list()
    for item in collection.find(kwargs):
        item.pop('_id')
        items.append(schema.from_query(item))
    if key is None:
        return items
    return {
        getattr(item, key): item for item in items
    }
