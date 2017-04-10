#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# build-in Exceptions
# ----------

from .utils import jrepr


class JasilyBaseException(Exception):
    def __init__(self, internal_error: str=None,
                 *args, **kwargs):
        super().__init__(*args)
        self._internal_error = internal_error
        self._kwargs = kwargs

    def __str__(self):
        return '<%s> %s' % (type(self).__name__, self._build_str_core())

    def _build_str_core(self):
        raise NotImplementedError

    @property
    def kwargs(self):
        return self._kwargs


class ApiNotSupportException(JasilyBaseException):
    ''''''
    def __init__(self, message: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = message

    def _build_str_core(self):
        return self._message


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


class ArgumentValueException(JasilyBaseException):
    def __init__(self, actual_value, except_message: str,
                 *args, **kwargs):
        '''you can use {value} to format value.'''
        super().__init__(*args, **kwargs)
        self._actual_value = actual_value
        self._except_message = except_message

    def _build_str_core(self):
        value = jrepr(self._actual_value)
        fmtext = self._except_message.format(value=value)
        return fmtext


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


