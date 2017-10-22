# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: 
# **********************************************************************************#


class BaseStation(object):
    """
    object of base station

    Args:
        identity(int): identity of base station
        cached_files(set): cached files
    """
    def __init__(self, identity, cached_files=set()):
        self.identity = identity
        self.cached_files = cached_files

    def caching_(self, files=set()):
        """
        Caching relevant files

        Args:
            files(set): files to be cached
        """
        self.cached_files |= files

    def clear(self):
        """
        Clear cached files
        """
        self.cached_files.clear()
