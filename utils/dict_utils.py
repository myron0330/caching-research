# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: dict utils
# **********************************************************************************#
from copy import copy


class DefaultDict(dict):

    """
    A dict that allows set default value for any key(exist or in-exist).
    """
    def __init__(self, default=None):
        """
        Args:
            default(class or object): the specified default type or instance.
        """
        super(DefaultDict, self).__init__()
        self._default = default

    def __missing__(self, key):
        default = self._default() if isinstance(self._default, type) else self._default
        self.__setitem__(key, copy(default))
        return self.__getitem__(key)
