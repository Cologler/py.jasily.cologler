#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

def jrepr(value):
    '''customized `repr()`.'''
    t = type(value)
    if t.__repr__ != object.__repr__:
        return repr(value)
    return 'object ' + t.__name__

