#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
# the builtins type.
# this lib should never import any library.
# ----------

import sys

def init():
    b = __builtins__
    bm = dict([('global_' + k, b[k]) for k in b])
    s = sys.modules[__name__].__dict__
    s.update(**bm)

init()
