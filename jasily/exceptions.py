#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# build-in Exceptions
# ----------

from inspect import Parameter
from .utils import jrepr


class BaseException(Exception):
    def __init__(self, message: str=None, inner_exception=None, *args, **kwargs):
        super().__init__(*args)
        self._message = message
        self._inner_exception = inner_exception
        self._kwargs = kwargs

    def __str__(self):
        return '{}: {}'.format(type(self).__name__, self.message)

    @property
    def message(self):
        return self._message or ''

    @property
    def kwargs(self):
        return self._kwargs


class ArgumentException(BaseException):
    '''base Exception for argument error.'''
    def __init__(self,
                 message: str,
                 parameter: (Parameter, str)=None,
                 inner_exception=None,
                 *args, **kwargs):
        super().__init__(message, inner_exception=inner_exception, *args, **kwargs)
        name = self._get_parameter_name(parameter)
        self._name = name

    @property
    def name(self):
        '''The name of parameter. canbe null.'''
        return self._name

    def _get_parameter_name(self, parameter: (Parameter, str)=None):
        if parameter is None:
            return None
        elif isinstance(parameter, Parameter):
            return parameter.name
        else:
            return str(parameter)


class ArgumentValueException(ArgumentException):
    pass


class ArgumentNoneException(ArgumentValueException):
    def __init__(self, message: str=None, *args, **kwargs):
        message = message or 'parameter <{}> cannot be `None`.'
        super().__init__(message)


class ArgumentTypeException(ArgumentException):
    def __init__(self,
                 except_type, actual_value,
                 parameter: (Parameter, str)=None,
                 *args, **kwargs):
        if not isinstance(except_type, type):
            raise ArgumentTypeException(type, except_type)
        param_name = self._get_parameter_name(parameter)
        if param_name is None:
            msg = 'param value type error:'
        else:
            msg = 'param <{}> value type error:'.format(param_name)
        actual_type = "'None'" if actual_value is None else type(actual_value).__name__
        except_type = except_type.__name__
        msg += ' (expected <{}>, got <{}>)'.format(except_type, actual_type)
        super().__init__(msg, parameter=param_name)


class InvalidArgumentException(BaseException):
    def __init__(self, parameter_name: str,
                 *args, **kwargs):
        super().__init__('', parameter_name, *args, **kwargs)


class ApiNotSupportException(BaseException):
    '''
    this is a little like `NotImplementedError`,
    but we donot want to impl it.
    '''


class InvalidOperationException(BaseException):
    '''a Exception define for invalid operation.'''
    def __init__(self, message: str=None,
                 *args, **kwargs):
        super().__init__(message or '', *args, **kwargs)

