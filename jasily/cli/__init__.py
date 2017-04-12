#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .exceptions import ParameterException
from .core import EngineBuilder


def fire(obj):
    '''same with `EngineBuilder().add(obj).build()`'''
    return EngineBuilder().add(obj).build()


__all__ = [
    'fire', 'EngineBuilder', 'ParameterException'
]

