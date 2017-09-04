#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

def object_has_no_attr(cls, attr):
    '''
    raise when object has no attribute.
    '''
    raise AttributeError("'{}' object has no attribute '{}'".format(cls.__name__, attr))

