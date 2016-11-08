#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# build-in Exceptions
# ----------

class ArgumentException(Exception):
    '''a Exception define for argument error.'''
    def __init__(self, parameter_name: str=None, message: str=None):
        super().__init__()
        self._parameter_name = parameter_name
        self._message = message or ''

    def __str__(self):
        if self._parameter_name is None:
            return self._message
        else:
            return '[ERROR ON PARAMETER %s] %s' % (self._parameter_name, self._message)

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