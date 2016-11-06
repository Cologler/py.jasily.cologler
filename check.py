#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import typing
import inspect
from inspect import signature
from inspect import Parameter
from .exceptions import InvalidOperationException

def _check_callable(func):
    if not callable(func):
        raise TypeError('func is not a callable object.')

def _raise(parameter_name, value, expected_type):
    if isinstance(expected_type, tuple):
        expected_type_name = '/'.join([x.__name__ for x in expected_type])
    else:
        expected_type_name = expected_type.__name__
    raise TypeError("parameter [%s] type error (expected %s, got %s)" % (
        parameter_name, expected_type_name, type(value).__name__))

def _check_type(name, value, expected_type, raise_error=True):
    if expected_type is None:
        expected_type = type(None)
    if isinstance(value, expected_type):
        return True
    if raise_error:
        _raise(name, value, expected_type)
    else:
        return False

class _TypeChecker:
    def __init__(self, name: str, annotation):
        self._name = name
        self._annotation = annotation

    @property
    def name(self):
        '''get parameter name.'''
        return self._name

    def check(self, value):
        '''check for argument.'''
        if self._annotation != Parameter.empty:
            _check_type(self._name, value, self._annotation)
        return value

def __build_checkers(parameters: typing.List[Parameter]):
    for parameter in parameters:
        yield _TypeChecker(parameter.name, parameter.annotation)

def __wrap(wrapper, func):
    '''make wrapper sign same as func.'''
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    # black technology
    wrapper.__signature__ = inspect.Signature.from_callable(func)
    return wrapper

def check_arguments(func):
    '''
    check function arguments by annotation.
    '''
    _check_callable(func)
    sign = signature(func)
    checkers = list(__build_checkers(sign.parameters.values()))
    checkers_map = dict(zip([x.name for x in checkers], checkers))
    def _wrapper(*args, **kwargs):
        for index, checker in enumerate(checkers[:len(args)]):
            checker.check(args[index])
        for name in kwargs:
            checker = checkers_map.get(name)
            if checker != None:
                checker.check(kwargs[name])
        return func(*args, **kwargs)
    return __wrap(_wrapper, func)

def check_return(func):
    '''
    check function return value by annotation.
    '''
    _check_callable(func)
    expected_type = func.__annotations__.get('return')
    if expected_type is None:
        raise InvalidOperationException('func does not contains return value annotation.')
    checker = _TypeChecker('return value', expected_type)
    def _wrapper(*args, **kwargs):
        return checker.check(func(*args, **kwargs))
    return __wrap(_wrapper, func)
