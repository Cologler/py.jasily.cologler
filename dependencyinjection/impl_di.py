#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import threading
from enum import Enum
from .impl_invoker import (
    check_type,
    NOT_FOUND,
    IValueFactory,
    SingletonValueFactory,
    Resolver
)

LOCK_SINGLETON = threading.Lock()

class LifeTime(Enum):
    singleton = 0
    scoped = 1
    transient = 2

class IValueStore:
    def get(self, key):
        '''get value or NOT_FOUND.'''
        raise NotImplementedError

    def set(self, key, value):
        '''set value for key.'''
        raise NotImplementedError

class DictValueStore(IValueStore):
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self.get(key, NOT_FOUND)

    def set(self, key, value):
        self._data[key] = value

class FactoryValueStore(IValueStore):
    def __init__(self, factory: IValueFactory):
        self._factory = factory
        self._is_singleton = isinstance(factory, SingletonValueFactory)
        self._value = NOT_FOUND

    def get(self, key):
        return self._value

    def set(self, key, value):
        self._value = value

class LifeTimeResolver(Resolver):
    '''resolver with life time.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._kwargs = kwargs
        self._cached_scopeds = DictValueStore()

    def provide(self, factory: IValueFactory,
                provide_type: type=None, provide_name: str=None, **kwargs):
        lifetime = kwargs.get('lifetime')
        check_type(lifetime, LifeTime)
        super().provide(factory, provide_type, provide_name)
        setattr(factory, 'lifetime', lifetime)
        if lifetime == LifeTime.singleton:
            setattr(factory, 'value_store', FactoryValueStore(factory))

    def _get_cached(self, factory: IValueFactory, lifetime: LifeTime) -> IValueStore:
        if lifetime == LifeTime.singleton:
            return getattr(factory, 'value_store')
        elif lifetime == LifeTime.scoped:
            return self._cached_scopeds
        else:
            return None

    def resolve(self, parameter_name: str, expected_type: type=None) -> object:
        '''
        resolve value for request parameter.
        return NOT_FOUND if not resolved.
        '''
        factory = self.resolve_factory(parameter_name, expected_type)
        if factory:
            lifetime = getattr(factory, 'lifetime')
            cached = self._get_cached(factory, lifetime)
            if cached != None:
                value = cached.get(factory, NOT_FOUND)
                if value != NOT_FOUND:
                    return value
            value = factory.value()
            if cached != None:
                cached.set(factory, value)
            return value
        else:
            return NOT_FOUND

    def clone(self):
        resolver = LifeTimeResolver(**self._kwargs)
        resolver.import_from(self)
        return resolver

raise NotImplementedError('current impl cache with lifetime.')

