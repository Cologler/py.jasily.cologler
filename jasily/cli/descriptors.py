#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

from .wrappers import wrap

G_TYPE = type

class Descriptor:
    def __init__(self, obj):
        self._obj = obj
        self._name: str = None
        self._type: G_TYPE = None

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

    def instance(self):
        raise NotImplementedError


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

