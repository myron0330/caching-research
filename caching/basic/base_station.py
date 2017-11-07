# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Base station file
# **********************************************************************************#
from .. utils.dict_utils import DefaultDict


class BaseStation(object):
    """
    object of base station

    Args:
        identity(int): identity of base station
        cached_files(set): cached files
    """
    def __init__(self, identity, cached_files=set(), memory=0):
        self.identity = identity
        self.cached_files = cached_files
        self.memory = memory
        self.demand_statics = dict()

    def caching_(self, files=set(), reset=True):
        """
        Caching relevant files

        Args:
            files(set): files to be cached
            reset(boolean): whether to clear cached other files
        """
        if reset:
            self.clear()
        self.cached_files |= files

    def observe_(self, demands=list()):
        """
        Loading demands statistics
        """
        results = DefaultDict(default=0)
        for demand in demands:
            results[demand - 1] += 1
        self.demand_statics = results

    def clear(self):
        """
        Clear cached files
        """
        self.cached_files.clear()
