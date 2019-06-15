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


class Counter(SyncedBox):
    '''thread safety counter.'''

    def __init__(self, init_value=0):
        super().__init__(init_value)

    def incr(self, value=1):
        '''return new value.'''
        return self.do(lambda x: x + value)

    def decr(self, value=1):
        '''return new value.'''
        return self.do(lambda x: x - value)

    def __enter__(self):
        self.incr()
        return self

    def __exit__(self, *args):
        self.decr()
        return False

    def __int__(self):
        return self.value
