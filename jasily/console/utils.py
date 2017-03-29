#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

class _UnbufferedStream(object):
    def __init__(self, stream):
        self._inner_stream = stream

    def write(self, data):
        '''override base method.'''
        self._inner_stream.write(data)
        self._inner_stream.flush()

    def __getattr__(self, attr):
        return getattr(self._inner_stream, attr)

    @property
    def inner_stream(self):
        '''get inner stream.'''
        return self._inner_stream

def stdout_disable_buffer():
    '''disable buffer for stdout.'''
    stream = sys.stdout
    if stream is None:
        return
    if not isinstance(stream, _UnbufferedStream):
        sys.stdout = _UnbufferedStream(stream)

def stdout_enable_buffer():
    '''enable buffer for stdout.'''
    stream = sys.stdout
    if stream is None:
        return
    if isinstance(stream, _UnbufferedStream):
        sys.stdout = stream.inner_stream

