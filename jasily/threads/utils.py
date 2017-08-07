#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import threading

class Counter():
    '''thread safety counter.'''

    def __init__(self, init_value=0):
        self._lock = threading.Lock()
        self._counter = init_value

    def incr(self, value=1):
        '''return new value.'''
        with self._lock:
            self._counter += value
            return self._counter

    def decr(self, value=1):
        '''return new value.'''
        with self._lock:
            self._counter -= value
            return self._counter

    @property
    def value(self):
        return self._counter

    def __enter__(self):
        self.incr()
        return self

    def __exit__(self, *args):
        self.decr()
        return False
