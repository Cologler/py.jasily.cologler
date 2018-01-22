#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from functools import update_wrapper

def readonly(obj, *, error_on_set = False):
    '''
    return a readonly proxy for the `obj`.

    all modify on the proxy will not apply on origin object.
    '''
    base_cls = type(obj)

    class Readonly(base_cls):
        def __getattribute__(self, name):
            return getattr(obj, name)

        def __setattr__(self, name, value):
            if error_on_set:
                raise AttributeError('cannot set readonly object.')

    update_wrapper(Readonly, base_cls, updated = ())
    return Readonly()
