#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .typed import ISession, IEngine
from .exceptions import RuntimeException
from .core import EngineBuilder


def fire(obj):
    '''same with `EngineBuilder().add(obj).build()`'''
    return EngineBuilder().add(obj).build()


__all__ = [
    'ISession', 'IEngine',
    'fire', 'EngineBuilder', 'RuntimeException'
]

