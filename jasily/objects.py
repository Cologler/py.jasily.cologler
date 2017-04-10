#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import uuid
from .exceptions import InvalidOperationException

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


class UInt:
    def __init__(self, value: int):
        v = int(value)
        if v < 0:
            raise ValueError
        self._value = v

    def __int__(self):
        return self._value

    def __eq__(self, value):
        return self._value == value

    @property
    def value(self):
        return self._value


class Set(set):
    def add(self, v):
        if v in self:
            return False
        set.add(self, v)
        return True


