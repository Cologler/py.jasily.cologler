#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------


from ..exceptions import (
    ArgumentNoneException,
    ArgumentValueException
)

from .test import *


def ensure_not_None(obj, name: str):
    '''raise `ArgumentNoneException` if obj is None.'''
    if obj is None:
        raise ArgumentNoneException('obj')

def ensure_enumerable(obj, name: str):
    '''raise `ArgumentValueException` if obj cannot enumerate.'''
    if not is_enumerable(obj):
        raise ArgumentValueException('obj', obj, '{value} is not enumerable.')

