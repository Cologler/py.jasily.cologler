#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

def __add_msg(func, msg, is_header: bool):
    if hasattr(func, '__doc__'):
        doc = getattr(func, '__doc__') or ''
    else:
        doc = ''
    if len(doc) == 0:
        doc = msg
    elif is_header:
        doc = msg + '\r\n' + doc
    else:
        doc = doc + '\r\n' + msg
    setattr(func, '__doc__', doc)

def thread_safely(func):
    '''declare function is thread safely.'''
    __add_msg(func, '[Thread-Safely]', True)
    return func

def thread_not_safely(func):
    '''declare function is thread not safely.'''
    __add_msg(func, '[Thread-NOT-Safely]', True)
    return func


