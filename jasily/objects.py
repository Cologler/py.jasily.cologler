#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import uuid
from .exceptions import InvalidOperationException

GUID_PY = 'py'
GUID_NET = 'net'

class __NotFound:
    '''a object for not found value.'''
    pass

NOT_FOUND = __NotFound()

class ValueContainer:
    def __init__(self, *args):
        self.__has_value = False
        self.__value = None
        if len(args) == 1:
            self.set_value(args[0])
        elif len(args) > 0:
            raise TypeError('only accept zero or one args.')

    @property
    def has_value(self):
        '''whether if container has value.'''
        return self.__has_value

    @property
    def value(self):
        '''get current value or None.'''
        return self.__value

    def set_value(self, value):
        '''set container value.'''
        self.__has_value = True
        self.__value = value

    def unset_value(self):
        '''remove container value.'''
        self.__has_value = False
        self.__value = None


class Guid:
    def __init__(self, uid=None, mode=GUID_PY):
        if uid is None:
            uid = uuid.uuid4()
        elif isinstance(uid, str):
            uid = uuid.UUID(uid)
        assert isinstance(uid, uuid.UUID)
        assert mode in [GUID_PY, GUID_NET]
        self._uuid = uid
        self._mode = mode

    def __str__(self):
        return str(self._uuid)

    def to_string(self):
        '''str(self)'''
        return str(self)

    def convert_to_net(self):
        '''convert to .net style guid.'''
        if self._mode == GUID_NET:
            return self
        if self._mode == GUID_PY:
            value = str(self)
            converted = value[6:8] + value[4:6] + value[2:4] + value[0:2] +\
                        value[8] + value[11:13] + value[9:11] + value[13] +\
                        value[16:18] + value[14:16] + value[18:]
            return Guid(converted)
        raise NotImplementedError

    def convert_to_py(self):
        '''convert to python style guid.'''
        if self._mode == GUID_PY:
            return self
        if self._mode == GUID_NET:
            return Guid(self._uuid, GUID_PY).convert_to_net()
        raise NotImplementedError


__FREEZABLE_FLAG = '__JASILY_FREEZABLE_IS_FREEZED__'

class Freezable:
    '''provide a freezable check base class.'''
    def freeze(self):
        '''freeze object.'''
        setattr(self, __FREEZABLE_FLAG, True)

    @property
    def is_freezed(self):
        '''check if freezed.'''
        return getattr(self, __FREEZABLE_FLAG, False)

    def _raise_if_freezed(self):
        '''raise `InvalidOperationException` if is freezed.'''
        if self.is_freezed:
            raise InvalidOperationException('obj is freezed.')
