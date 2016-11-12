#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

def dict_setdefault(source: dict, key, factory: callable, default_test=None):
    ret = source.get(key, default_test)
    if ret is default_test:
        ret = factory()
        source[key] = ret
    return ret




