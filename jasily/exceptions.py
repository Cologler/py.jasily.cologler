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
        return '<%s> %s' % (type(self).__name__, self.message)

    @property
    def message(self):
        return ''

    @property
    def kwargs(self):
        return self._kwargs


class MessageException(JasilyBaseException):
    def __init__(self, message: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = message

    @property
    def message(self):
        return (self._message  or '').format(**self.kwargs)

    def __str__(self):
        return self.message


class ArgumentException(MessageException):
    '''a Exception for argument error.'''
    def __init__(self, message: str, parameter_name: str=None,
                 *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self._parameter_name = parameter_name
        self.kwargs['parameter_name'] = parameter_name


class ArgumentTypeException(ArgumentException):
    def __init__(self, except_type, actual_value,
                 *args, **kwargs):
        if not isinstance(except_type, type):
            raise ArgumentTypeException(type, except_type)
        actual_type = "'None'" if actual_value is None else type(actual_value).__name__
        fmtext = 'param <{parameter_name}> value type error:'
        fmtext += ' (expected <{except_type}>, got <{actual_type}>)'
        fmtext = 'param <{parameter_name}> value type error:' +\
                 ' (expected <{except_type}>, got <{actual_type}>)'
        super().__init__(fmtext,
                         parameter_name=kwargs.get('parameter_name', '?'),
                         except_type=except_type.__name__,
                         actual_type=actual_type,
                         *args, **kwargs)


class ArgumentValueException(MessageException):
    def __init__(self, actual_value,
                 *args, **kwargs):
        '''you can use {value} to format value.'''
        super().__init__(*args, **kwargs)
        self._actual_value = actual_value
        value = jrepr(self._actual_value)
        self.kwargs['value'] = value


class InvalidArgumentException(MessageException):
    def __init__(self, parameter_name: str,
                 *args, **kwargs):
        super().__init__('', parameter_name, *args, **kwargs)


class ApiNotSupportException(MessageException):
    '''
    this is a little like `NotImplementedError`,
    but we donot want to impl it.
    '''


class InvalidOperationException(MessageException):
    '''a Exception define for invalid operation.'''
    def __init__(self, message: str=None,
                 *args, **kwargs):
        super().__init__(message or '', *args, **kwargs)

