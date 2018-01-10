# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#
from pymongo import MongoClient, UpdateOne


client = MongoClient('localhost', 27017)
database = client['iqiyi']
category_collection = database['category']
album_collection = database['album']
video_collection = database['video']


class Collections(object):

    category = category_collection
    album = album_collection
    video = video_collection


class MongodbBatch(object):

    def __init__(self, collection, buffer_size=2000):
        self.buffer_size = buffer_size
        self.buffer = []
        self.collection = collection

    def append(self, query, update):
        self.buffer.append(UpdateOne(query, update, upsert=True))
        self.check_and_commit()

    def check_and_commit(self):
        if len(self.buffer) == self.buffer_size:
            self.commit()

    def commit(self):
        if self.buffer:
            self.collection.bulk_write(self.buffer, ordered=False)
            del self.buffer[:]

    def end(self):
        self.commit()


class BatchOps(object):

    category = MongodbBatch(Collections.category)
    album = MongodbBatch(Collections.album)
    video = MongodbBatch(Collections.video)
