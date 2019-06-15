#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import threading

class SyncedBox:
    def __init__(self, init_value):
        self._value = init_value
        self._lock = threading.RLock()

    def do(self, func):
        with self._lock:
            self._value = func(self._value)
            return self._value

    @property
    def value(self):
        with self._lock:
            return self._value


class Counter:
    '''thread safety counter.'''

    __slots__ = ('_value', '_lock', '__weakref__')

    def __init__(self, init_value: int=0):
        self._value = init_value
        self._lock = threading.Lock()

    def incr(self, value=1):
        '''
        add value in this `Counter` and return current value.
        '''
        with self._lock:
            self._value += value
            return self._value

    def decr(self, value=1):
        '''
        sub value in this `Counter` and return current value.
        '''
        with self._lock:
            self._value -= value
            return self._value

    def __iadd__(self, value):
        self.incr(value)

    def __isub__(self, value):
        self.decr(value)

    @property
    def value(self):
        with self._lock:
            return self._value

    def __enter__(self):
        self += 1
        return self

    def __exit__(self, *args):
        self -= 1
        return False

    def __int__(self):
        return self.value
