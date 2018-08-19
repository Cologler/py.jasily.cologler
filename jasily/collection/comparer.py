# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# a comparer like csharp
# ----------

from abc import abstractmethod

class IComparer:
    '''
    the comparer interface.
    '''
    @abstractmethod
    def hash(self, obj):
        '''
        get the hash from object.
        '''
        raise NotImplementedError

    @abstractmethod
    def eq(self, obj1, obj2):
        '''
        compare two value is equals or not.
        '''
        raise NotImplementedError


class ObjectComparer(IComparer):
    '''
    the default comparer implemention for object.
    '''
    def hash(self, obj):
        return hash(obj)

    def eq(self, obj1, obj2):
        return obj1 == obj2


class Wrap:
    '''
    wrap a object with given comparer.
    '''

    def __init__(self, comparer, obj):
        self._comparer = comparer
        self._obj = obj

    def unwrap(self):
        '''
        get the origin object.
        '''
        return self._obj

    def __hash__(self):
        return self._comparer.hash(self._obj)

    def __eq__(self, other):
        '''
        note: user should ensure other is instance of Wrap.
        '''
        return self._comparer.eq(self._obj, other.unwrap())


class IgnoreCaseStringComparer(IComparer):
    def hash(self, obj: str):
        return hash(obj.upper())

    def eq(self, obj1: str, obj2: str):
        return obj1.upper() == obj2.upper()
