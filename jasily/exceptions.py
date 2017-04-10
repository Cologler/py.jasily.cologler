#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# build-in Exceptions
# ----------


class JasilyBaseException(Exception):
    def __str__(self):
        return '<%s> %s' % (type(self).__name__, self._build_str_core())

    def _build_str_core(self):
        raise NotImplementedError


class ArgumentException(JasilyBaseException):
    '''a Exception for argument error.'''
    def __init__(self, parameter_name: str=None, message: str=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parameter_name = parameter_name
        self._message = message or ''

    def _build_str_core(self):
        if self._parameter_name is None:
            return self._message
        else:
            return '[ERROR ON PARAMETER %s] %s' % (self._parameter_name, self._message)


class ArgumentTypeException(ArgumentException):
    def __init__(self, except_type, actual_value,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(except_type, type):
            raise ArgumentTypeException(type, except_type)
        self._except_type = except_type
        self._actual_value = actual_value

    def _build_str_core(self):
        actual_type = "'None'" if self._actual_value is None else type(self._actual_value).__name__

        fmtext = 'param <{name}> value type error:'
        fmtext += ' (expected <{except_type}>, got <{actual_type}>)'
        return fmtext.format(name=self._parameter_name or '?',
                             except_type=self._except_type.__name__,
                             actual_type=actual_type)


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
    'InvalidOperationException',
    'ArgumentTypeException'
]


