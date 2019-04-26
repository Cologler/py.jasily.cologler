# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod
import typing

from .box import Box

T = typing.TypeVar('T')

class IVar(ABC, typing.Generic[T]):
    __slots__ = ()

    @property
    @abstractmethod
    def has_value(self):
        '''get whether var has value or not.'''
        raise NotImplementedError

    @abstractmethod
    def get(self, default=None):
        '''get and value.'''
        raise NotImplementedError

    @abstractmethod
    def pop(self, default=None):
        '''get and remove value.'''
        raise NotImplementedError

    @abstractmethod
    def set(self, value):
        '''set value.'''
        raise NotImplementedError

    @abstractmethod
    def set_default(self, value):
        '''set value if does not exists.'''
        raise NotImplementedError


class BoxVar(IVar):
    '''a static var that store in a `Box`'''

    __slots__ = ('_box')

    def __init__(self, box: Box):
        self._box = box

    def has_value(self):
        '''get whether var has value or not.'''
        return self._box.has_value

    def get(self, default=None):
        '''get and value.'''
        return self._box.get(default)

    def pop(self, default=None):
        '''get and remove value.'''
        ret = self._box.get(default)
        self._box.reset()

    def set(self, value):
        '''set value.'''
        self._box.value = value

    def set_default(self, value):
        '''set value if does not exists.'''
        if not self._box.has_value:
            self._box.value = value


class AttrVar(IVar):
    '''a var that store in object attrs'''

    __slots__ = ('_obj', '_key')

    def __init__(self, obj, key):
        self._obj = obj
        self._key = key

    @property
    def has_value(self):
        '''get whether var has value or not.'''
        return hasattr(self._obj, self._key)

    def get(self, default=None):
        '''get and value.'''
        return getattr(self._obj, self._key, default)

    def pop(self, default=None):
        '''get and remove value.'''
        ret = getattr(self._obj, self._key, default)
        delattr(self._obj, self._key)
        return ret

    def set(self, value):
        '''set value.'''
        setattr(self._obj, self._key, value)

    def set_default(self, value):
        '''set value if does not exists.'''
        if self.has_value:
            self.set(value)


class DictVar(IVar):
    '''a var that store in `dict`'''

    __slots__ = ('_dict', '_key')

    def __init__(self, d: dict, key):
        self._dict = d
        self._key = key

    @property
    def has_value(self):
        '''get whether var has value or not.'''
        return self._key in self._dict

    def get(self, default=None):
        '''get and value.'''
        return self._dict.get(self._key, default)

    def pop(self, default=None):
        '''get and remove value.'''
        return self._dict.pop(self._key, default)

    def set(self, value):
        '''set value.'''
        self._dict[self._key] = value

    def set_default(self, value):
        '''set value if does not exists.'''
        self._dict.setdefault(self._key, value)


class FieldVar(DictVar):
    __slots__ = ()

    def __init__(self, obj, key):
        super().__init__(vars(obj), key)


def get_object_var_factory(obj):
    '''
    get default var factory for the object.

    return a func with sign: `(key) => IVar`
    '''
    def var_factory(key):
        try:
            return FieldVar(obj, key)
        except TypeError:
            return AttrVar(obj, key)

    return var_factory
