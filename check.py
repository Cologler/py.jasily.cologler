#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import inspect
from inspect import signature
from inspect import Parameter
from .exceptions import InvalidOperationException

def _get_func_name(func):
    if hasattr(func, '__name__'):
        return getattr(func, '__name__')
    return 'func'

def _check_callable(func):
    if not callable(func):
        name = _get_func_name(func)
        raise TypeError('%s is not a callable object.' % name)


class _ExpectedChecker:
    def check(self, value) -> bool:
        '''check if value match this checker.'''
        raise NotImplementedError
    def __str__(self) -> str:
        raise NotImplementedError

class _TypeExpectedChecker(_ExpectedChecker):
    def __init__(self, expected_type: type):
        self._expected_type = expected_type
    def check(self, value) -> bool:
        return isinstance(value, self._expected_type)
    def __str__(self) -> str:
        return self._expected_type.__name__

class _TypeTupleExpectedChecker(_ExpectedChecker):
    def __init__(self, expected_types: tuple):
        self._expected_types = expected_types
    def check(self, value) -> bool:
        return isinstance(value, self._expected_types)
    def __str__(self) -> str:
        return '/'.join([x.__name__ for x in self._expected_types])

class _CallableExpectedChecker(_ExpectedChecker):
    def __init__(self, expected_callable: tuple):
        self._expected_callable = expected_callable
        self._name = _get_func_name(expected_callable)
        self._sign = signature(expected_callable)
        if len(self._sign.parameters) != 1:
            raise InvalidOperationException(
                'function %s contains too many args (only support 1).' % self._name)
    def check(self, value) -> bool:
        return self._expected_callable(value)
    def __str__(self) -> str:
        return self._name + '()'

class _ComplexExpectedChecker(_ExpectedChecker):
    def __init__(self, expected_tuple: tuple):
        self._expected_tuple = expected_tuple
        expected_types = []
        expected_other = []
        for item in self._expected_tuple:
            if isinstance(item, type) or item is None:
                expected_types.append(item or type(None))
            else:
                expected_other.append(item)
        self._checkers = []
        if len(expected_types) > 0:
            self._checkers.append(_expected_checker(tuple(expected_types), False))
        if len(expected_other) > 0:
            self._checkers.append(_expected_checker(tuple(expected_other), False))
    def check(self, value) -> bool:
        for checker in self._checkers:
            if checker.check(value):
                return True
        return False
    def __str__(self):
        return '/'.join([str(x) for x in self._checkers])

def _expected_checker(annotation, allow_complex) -> _ExpectedChecker:
    if annotation == Parameter.empty:
        return None
    elif annotation is None:
        return _TypeExpectedChecker(type(None))
    elif isinstance(annotation, type):
        return _TypeExpectedChecker(annotation)
    elif isinstance(annotation, tuple):
        is_all_type = True
        for item in annotation:
            if not isinstance(item, type):
                is_all_type = False
                break
        if is_all_type:
            return _TypeTupleExpectedChecker(annotation)
        elif allow_complex:
            return _ComplexExpectedChecker(annotation)
    elif callable(annotation):
        return _CallableExpectedChecker(annotation)
    raise NotImplementedError('unknown annotation contract.')

class _AnnotationChecker:
    def __init__(self, name: str, annotation):
        self._name = name
        self._annotation = annotation
        if self._annotation is None:
            self._annotation = type(None)
        self._checker = _expected_checker(annotation, True)

    @property
    def name(self):
        '''get parameter name.'''
        return self._name

    def can_check(self):
        '''check if '''
        return self._checker != None

    def check(self, value):
        '''check for argument.'''
        if self.can_check():
            if not self._checker.check(value):
                self._raise_error(value)
        return value

    def _raise_error(self, value):
        raise TypeError("parameter [%s] type error (expected %s, got %s)" % (
            self._name, self._checker, type(value).__name__))

def _wrap(wrapper, func):
    '''make wrapper sign same as func.'''
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    # black technology
    wrapper.__signature__ = inspect.Signature.from_callable(func)
    return wrapper

def check_arguments(func):
    '''
    check function arguments by annotation.

    <cannot after @classmethod> please call before @classmethod like:
    @classmethod
    @check_arguments
    def method(cls):
        pass
    '''
    _check_callable(func)
    sign = signature(func)
    checkers = [_AnnotationChecker(x.name, x.annotation) for x in sign.parameters.values()]
    def _check():
        for checker in checkers:
            if checker.can_check():
                return
        name = _get_func_name(func)
        raise InvalidOperationException('%s does not contains any parameter annotation.' % name)
    _check()
    checkers_map = dict(zip([x.name for x in checkers], checkers))
    def _function(*args, **kwargs):
        for index, checker in enumerate(checkers[:len(args)]):
            checker.check(args[index])
        for name in kwargs:
            checker = checkers_map.get(name)
            if checker != None:
                checker.check(kwargs[name])
        return func(*args, **kwargs)
    return _wrap(_function, func)

def check_return(func):
    '''
    check function return value by annotation.

    <cannot after @classmethod> please call before @classmethod like:
    @classmethod
    @check_return
    def method(cls):
        pass
    '''
    _check_callable(func)
    expected_type = func.__annotations__.get('return')
    if expected_type is None:
        name = _get_func_name(func)
        raise InvalidOperationException('%s does not contains return value annotation.' % name)
    checker = _AnnotationChecker('return value', expected_type)
    def _function(*args, **kwargs):
        return checker.check(func(*args, **kwargs))
    return _wrap(_function, func)

__all__ = [
    'check_arguments',
    'check_return',
]