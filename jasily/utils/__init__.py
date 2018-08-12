#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

def jrepr(value):
    '''customized `repr()`.'''
    if value is None:
        return repr(value)
    t = type(value)
    if t.__repr__ is not object.__repr__:
        return repr(value)
    return 'object ' + t.__name__


def get_parent(obj):
    '''
    get parent from obj.
    '''
    names = obj.__qualname__.split('.')[:-1]
    if '<locals>' in names: # locals function
        raise ValueError('cannot get parent from locals object.')
    module = sys.modules[obj.__module__]
    parent = module
    while names:
        parent = getattr(parent, names.pop(0))
    return parent
