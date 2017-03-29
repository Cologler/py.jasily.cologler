#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
#
#
#

import threading

class Counter():
    '''thread safe counter.'''

    def __init__(self, init_value=0):
        self._lock = threading.Lock()
        self._counter = init_value

    def increment(self, value=1):
        '''return new value.'''
        with self._lock:
            self._counter += value
            return self._counter

    def decrement(self, value=1):
        '''return new value.'''
        with self._lock:
            self._counter -= value
            return self._counter

    @property
    def value(self):
        with self._lock:
            return self._counter

    def __enter__(self):
        self.increment()
        return self

    def __exit__(self, *args):
        self.decrement()
        return False