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
import typing
from .exceptions import InvalidOperationException

def _raise(actual_value: object, expected: (type, str)):
    expected_str = expected if isinstance(expected, str) else expected.__name__
    raise TypeError("type error (expected %s, got %s)" % (
        expected_str, type(actual_value).__name__))

def _types_to_str(types: typing.Tuple[type]):
    return '/'.join([x.__name__ for x in types])

def _is_generic_type(value: type):
    return isinstance(value, typing.TypingMeta)

def _get_func_name(func):
    return getattr(func, '__name__', 'func')

def check_callable(func):
    if callable(func):
        return
    name = _get_func_name(func)
    _raise(name, 'callable')

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
        return _types_to_str(self._expected_types)

class _CallableExpectedChecker(_ExpectedChecker):
    def __init__(self, expected_callable: callable):
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

def _expected_checker(annotation, allow_complex=True) -> _ExpectedChecker:
    if annotation == Parameter.empty:
        return None
    elif annotation is None:
        return _TypeExpectedChecker(type(None))
    elif isinstance(annotation, type):
        return _TypeExpectedChecker(annotation)
    elif isinstance(annotation, tuple):
        if len(annotation) == 1: # unpack
            return _expected_checker(annotation[0], allow_complex)
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

def _wrap(wrapper, func, sign=None):
    '''make wrapper sign same as func.'''
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    wrapper.__name__ = func.__name__
    wrapper.__signature__ = sign or inspect.Signature.from_callable(func)
    return wrapper

def check_arguments(func):
    '''
    check function arguments by annotation.

    e.g.1: allow str
    @check_arguments
    def function(arg: str): pass

    e.g.2: allow str or int
    @check_arguments
    def function(arg: (str, int)): pass

    e.g.3: is_xxx canbe a callable[object] ptr.
    @check_arguments
    def function(arg: (str, is_xxx)): pass

    <cannot after @classmethod> please call before @classmethod like:
    @classmethod
    @check_arguments
    def method(cls):
        pass
    '''
    check_callable(func)
    sign = signature(func)
    checkers = [_AnnotationChecker(x.name, x.annotation) for x in sign.parameters.values()]
    checkers_map = dict(zip([x.name for x in checkers], checkers))
    def _function(*args, **kwargs):
        for index, checker in enumerate(checkers[:len(args)]):
            checker.check(args[index])
        for name in kwargs:
            checker = checkers_map.get(name)
            if checker != None:
                checker.check(kwargs[name])
        return func(*args, **kwargs)
    return _wrap(_function, func, sign)

def check_return(func):
    '''
    check function return value by annotation.

    e.g.1: allow str
    @check_arguments
    def function() -> str: pass

    e.g.2: allow str or int
    @check_arguments
    def function() -> (str, int): pass

    e.g.3: is_xxx canbe a callable[object] ptr
    @check_arguments
    def function() -> (str, is_xxx): pass

    <cannot after @classmethod> please call before @classmethod like:
    @classmethod
    @check_return
    def method(cls):
        pass
    '''
    check_callable(func)
    expected_type = func.__annotations__.get('return', Parameter.empty)
    checker = _AnnotationChecker('return value', expected_type)
    def _function(*args, **kwargs):
        return checker.check(func(*args, **kwargs))
    return _wrap(_function, func)

@check_arguments
def check_generic(actual_value, expected_type: typing.TypingMeta):
    '''
    check if value match type.
    raise TypeError if not match.

    NOTE: check generic for collection will enumerate entire collection.
    '''
    _check_type(actual_value, expected_type, True)

@check_arguments
def check_type(actual_value, expected_type: type):
    '''
    check if value match type.
    raise TypeError if not match.
    '''
    _check_type(actual_value, expected_type, False)

def __is_instance_of_type(actual_value, expected_type: type,
                          include_generic: bool) -> bool:
    if isinstance(expected_type, tuple):
        return _is_instance_of_type_tuple(actual_value, expected_type, include_generic)
    if include_generic and _is_generic_type(expected_type):
        return _is_instance_of_generic_type(actual_value, expected_type)
    checker = _expected_checker(expected_type, True)
    return checker.check(actual_value)

def _is_instance_of_type_tuple(actual_value, expected_type: typing.Tuple[type],
                               include_generic: bool) -> bool:
    if include_generic:
        generics = []
        for that in expected_type:
            if _is_generic_type(that):
                generics.append(that)
        for that in generics:
            if _is_instance_of_generic_type(actual_value, that):
                return True
    checker = _expected_checker(expected_type, True)
    return checker.check(actual_value)

def _is_instance_of_generic_type(actual_value, expected_type: typing.TypingMeta):
    if expected_type._has_type_var():
        raise NotImplementedError('expected_type cannot contains type ver.')
    if isinstance(expected_type, typing.GenericMeta):
        parameters = expected_type.__parameters__
        if isinstance(actual_value, (list, set)):
            for item in actual_value:
                if not __is_instance_of_type(item, parameters[0], True):
                    return False
        elif isinstance(actual_value, dict):
            for key in actual_value:
                if not __is_instance_of_type(key, parameters[0], True):
                    return False
                if not __is_instance_of_type(actual_value[key], parameters[1], True):
                    return False
        else:
            raise NotImplementedError
    elif isinstance(expected_type, typing.TupleMeta):
        parameters = expected_type.__tuple_params__
        if len(actual_value) != len(parameters):
            expected_str = '(' + ', '.join([x.__name__ for x in parameters]) + ')'
            actual_str = '(' + ', '.join([type(x).__name__ for x in actual_value]) + ')'
            raise TypeError("type error (expected %s, got %s)" % (expected_str, actual_str))
        for left, right in zip(actual_value, parameters):
            if not __is_instance_of_type(left, right, True):
                return False
    else:
        raise NotImplementedError
    return True

def _check_type_tuple(actual_value, expected_type: typing.Tuple[type], include_generic: bool):
    if not _is_instance_of_type_tuple(actual_value, expected_type, include_generic):
        _raise(actual_value, expected_type)

def _check_type(actual_value, expected_type: type, include_generic: bool):
    if isinstance(expected_type, tuple):
        return _check_type_tuple(actual_value, expected_type, include_generic)
    if not __is_instance_of_type(actual_value, expected_type, include_generic):
        _raise(actual_value, expected_type)

__all__ = [
    # function
    'check_callable',
    'check_generic',

    # decorator
    'check_arguments',
    'check_return'
]