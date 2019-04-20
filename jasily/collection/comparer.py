# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# a comparer like csharp
# ----------

from abc import abstractmethod

class IEqualityComparer:
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
    def eq(self, cmpvalue_1, cmpvalue_2):
        '''
        compare two value is equals or not.
        '''
        raise NotImplementedError

    def get_cmpvalue(self, obj):
        '''
        get the cmpvalue use for eq compare.
        this is help to cache some value like `str.upper()`.
        '''
        return obj


class ObjectWrapper:
    '''
    wrap a object with given equality comparer.
    '''
    __slots__ = ('_comparer', '_obj', '_hashcode', '_cmpvalue')

    def __init__(self, comparer: IEqualityComparer, obj):
        self._comparer = comparer
        self._obj = obj
        self._hashcode = None
        self._cmpvalue = None

    def unwrap(self):
        '''
        get the origin object.
        '''
        return self._obj

    def __hash__(self):
        if self._hashcode is None:
            self._hashcode = self._comparer.hash(self._obj)
        return self._hashcode

    def get_cmpvalue(self):
        if self._cmpvalue is None:
            self._cmpvalue = (self._comparer.get_cmpvalue(self._obj), )
        return self._cmpvalue

    def __eq__(self, other):
        '''
        note: user should ensure other is instance of Wrap.
        '''
        return self._comparer.eq(self.get_cmpvalue(), other.get_cmpvalue())


class ObjectComparer(IEqualityComparer):
    '''
    the default comparer implemention for object.
    '''
    def hash(self, obj):
        return hash(obj)

    def eq(self, obj1, obj2):
        return obj1 == obj2


class IgnoreCaseStringComparer(IEqualityComparer):
    def hash(self, obj: str):
        return hash(obj.upper())

    def eq(self, cmpvalue_1, cmpvalue_2):
        return cmpvalue_1 == cmpvalue_1

    def get_cmpvalue(self, obj: str):
        return obj.upper()


class StringComparer:
    IgnoreCaseComparer = IgnoreCaseStringComparer()
