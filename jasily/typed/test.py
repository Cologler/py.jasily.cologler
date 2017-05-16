#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from inspect import signature


def is_enumerable(obj):
    if not hasattr(obj, '__iter__'):
        return False
    if len(signature(obj.__iter__).parameters) != 0:
        return False
    return True


