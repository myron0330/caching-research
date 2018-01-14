# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from uuid import uuid1
from mongo_base import Collections
from schema import *


def update_one_(collection, schema):
    """
    Update one schema
    """
    query_field, item = schema.to_mongodb_item()
    collection.update_one(query_field, item, upsert=True)


def query_from_(collection, key=None, fields=None, **kwargs):
    """
    Query from schemas from collection
    """
    if collection == Collections.category:
        schema = CategorySchema
    elif collection == Collections.album:
        schema = AlbumSchema
    else:
        raise Exception('Schema Error')
    items = list()
    if fields:
        for item in collection.find(kwargs, fields):
            item.pop('_id')
            items.append(item)
        return items
    for item in collection.find(kwargs):
        item.pop('_id')
        items.append(schema.from_query(item))
    if key is None:
        return items
    return {
        getattr(item, key): item for item in items
    }


def dump_to_(batch_op, schema, unit_dump=True):
    """
    Dump schema to mongodb

    Args:
        batch_op(obj): schema type
        schema(schema or list, dict of schema): schema object
        unit_dump(boolean): whether to do unit dump
    """
    if isinstance(schema, list):
        for _ in schema:
            batch_op.append(*_.to_mongodb_item())
    else:
        schema_iter = schema if isinstance(schema, dict) else {str(uuid1()): schema}
        for _, schema in schema_iter.iteritems():
            batch_op.append(*schema.to_mongodb_item())
    if unit_dump:
        batch_op.commit()
