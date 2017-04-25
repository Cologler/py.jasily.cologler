#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from .typed import (
    ISession, IEngine,
    IFile, IFolder
)
from .exceptions import RuntimeException
from .core import EngineBuilder


def fire(obj, argv=sys.argv, **kwargs):
    '''same with `EngineBuilder().add(obj).build().execute(sys.argv)`'''
    engine = EngineBuilder().add(obj).build()
    return engine.execute(argv, **kwargs)


__all__ = [
    'ISession', 'IEngine',
    'IFile', 'IFolder',
    'fire', 'EngineBuilder', 'RuntimeException'
]

