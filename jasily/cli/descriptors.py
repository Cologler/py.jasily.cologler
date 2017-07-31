#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

from ..g import global_type
from .wrappers import wrap


class Descriptor:
    def __init__(self, obj):
        self._obj = obj
        self._name: str = None
        self._type: global_type = None
        self._alias: list = None
        self._doc: str = getattr(obj, '__doc__', '')

    @property
    def doc(self):
        '''get doc from command descriptor.'''
        return self._doc

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        '''canbe `None`'''
        return self._type

    @property
    def described_object(self):
        return self._obj

    def enumerate_names(self):
        yield self._name
        if self._alias:
            for n in self._alias:
                yield n

    def instance(self):
        raise NotImplementedError

    def add_alias(self, s: str):
        if self._alias is None:
            self._alias = []
        self._alias.append(s)


class TypeDescriptor(Descriptor):
    def __init__(self, type):
        super().__init__(type)
        self._name: str = type.__name__
        self._type = type

    def instance(self):
        return self._type()


class InstanceDescriptor(Descriptor):
    def __init__(self, obj):
        super().__init__(obj)
        self._type = type(obj)

    def instance(self):
        return self._obj


class CallableDescriptor(Descriptor):
    def __init__(self, func):
        super().__init__(func)
        self._name: str = func.__name__


class PropertyDescriptor(Descriptor):
    def __init__(self, prop, name):
        super().__init__(prop)
        self._name: str = name


def describe(obj, name=None):
    if isinstance(obj, Descriptor):
        return obj
    elif isinstance(obj, type):
        return TypeDescriptor(obj)
    elif callable(obj):
        return CallableDescriptor(obj)
    elif isinstance(obj, property):
        return PropertyDescriptor(obj, name)
    else:
        return InstanceDescriptor(wrap(obj))

