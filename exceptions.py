#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# build-in Exceptions
# ----------

class InvalidOperationException(Exception):
    '''a Exception define for invalid operation.'''

    def __init__(self, message: str=None):
        super().__init__()
        self._message = message or ''

    def __str__(self):
        return self._message

    @property
    def message(self):
        '''get message.'''
        return self._message




__all__ = [
    'InvalidOperationException'
]