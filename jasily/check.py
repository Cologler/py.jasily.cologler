#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import inspect
from inspect import signature, Parameter
import typing
from .exceptions import InvalidOperationException

G_TYPE = type

def _raise(actual_value: object, expected: (type, str)):
    expected_str = expected if isinstance(expected, str) else expected.__name__
    raise TypeError("type error (expected %s, got %s)" % (
        expected_str, type(actual_value).__name__))

def _get_func_name(func):
    return getattr(func, '__name__', 'func')

class _Checker:
    def check(self, value) -> bool:
        '''check if value match this checker.'''
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    @staticmethod
    def create(annotation, allow_complex=True):
        if annotation == Parameter.empty:
            return None
        elif annotation is None:
            return _TypeChecker(type(None))
        elif isinstance(annotation, typing.GenericMeta):
            if annotation.__origin__ in (typing.List, typing.Set):
                assert len(annotation.__args__) == 1
                t = annotation.__args__[0]
                return _TypedCollectionChecker(annotation, t)
            elif annotation.__origin__ is typing.Dict:
                k, v = annotation.__args__
                return _TypedDictChecker(annotation, k, v)
            else:
                NotImplementedError('unknown typing.GenericMeta: <%s>' % annotation)
        elif isinstance(annotation, typing.TupleMeta):
            if annotation.__origin__ is typing.Tuple:
                return _TypedTupleChecker(annotation, annotation.__args__)
            else:
                NotImplementedError('unknown typing.TupleMeta: <%s>' % annotation)
        elif isinstance(annotation, type):
            return _TypeChecker(annotation)
        elif isinstance(annotation, (tuple, list)):
            if len(annotation) == 1: # unpack
                return _Checker.create(annotation[0], allow_complex)
            if all([isinstance(z, type) for z in annotation]):
                return _TupleChecker(annotation)
            elif allow_complex:
                return _ComplexChecker(annotation)
            else:
                return None
        elif callable(annotation):
            return _CallableChecker(annotation)
        raise NotImplementedError('unknown annotation contract.')


class _TypeChecker(_Checker):
    def __init__(self, type):
        self._type = type

    def check(self, value) -> bool:
        return isinstance(value, self._type)

    def __str__(self) -> str:
        return self._type.__name__


class _TupleChecker(_Checker):
    def __init__(self, types: tuple):
        self._types = tuple(types) # types maybe list.

    def check(self, value) -> bool:
        return isinstance(value, self._types)

    def __str__(self) -> str:
        return '/'.join([x.__name__ for x in self._types])


class _CallableChecker(_Checker):
    def __init__(self, callable: callable):
        self._callable = callable
        self._name = _get_func_name(callable)
        self._sign = signature(callable)
        if len(self._sign.parameters) != 1:
            raise InvalidOperationException(
                'function %s contains too many args (only support 1).' % self._name)

    def check(self, value) -> bool:
        return self._callable(value)

    def __str__(self) -> str:
        return self._name + '()'


class _ComplexChecker(_Checker):
    def __init__(self, items: tuple):
        types = []
        other = []
        for item in items:
            if isinstance(item, type):
                types.append(item)
            else:
                other.append(item)
        self._checkers = []
        if len(types) > 0:
            self._checkers.append(_Checker.create(tuple(types), False))
        if len(other) > 0:
            self._checkers.append(_Checker.create(tuple(other), False))

    def check(self, value) -> bool:
        if len(self._checkers) == 0:
            return True
        return any([c.check(value) for c in self._checkers])

    def __str__(self):
        return '/'.join([str(x) for x in self._checkers])


class _GenericChecker(_Checker):
    def __init__(self, type, t):
        self._type = type

    def check(self, value) -> bool:
        if not isinstance(self._type):
            return False
        return self._check_items(value)

    def _check_items(self, items) -> bool:
        raise NotImplementedError


class _TypedCollectionChecker(_GenericChecker):
    def __init__(self, type, t):
        super().__init__(type)
        self._t = t

    def _check_items(self, items) -> bool:
        for t in items:
            if not isinstance(t, self._t):
                return False
        return True


class _TypedDictChecker(_GenericChecker):
    def __init__(self, type, keytype, valuetype):
        super().__init__(type)
        self._k = keytype
        self._v = valuetype

    def _check_items(self, items) -> bool:
        for t in items.keys():
            if not isinstance(t, self._k):
                return False
        for t in items.values():
            if not isinstance(t, self._v):
                return False
        return True


class _TypedTupleChecker(_GenericChecker):
    def __init__(self, type, types):
        super().__init__(type)
        self._types = tuple(types)

    def _check_items(self, items) -> bool:
        if len(self._types) != len(items):
            return False
        for i in range(0, self._types):
            if not isinstance(items[i], self._types[i]):
                return False
        return True


class AnnotationChecker:
    def __init__(self, name: str, annotation):
        self._name = name
        self._annotation = annotation
        if self._annotation is None:
            self._annotation = type(None)
        self._checker = _Checker.create(annotation, True)

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
        name = self.name
        if name == 'return':
            name = 'return value'
        else:
            name = 'parameter <%s>' % name
        raise TypeError("%s type error (expected %s, got %s)" % (
            self.name, self._checker, type(value).__name__))


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
    def method(cls): pass
    '''
    sign = signature(func)
    annotations = [x for x in sign.parameters.values() if x.annotation != Parameter.empty]
    checkers = [AnnotationChecker(x.name, x.annotation) for x in annotations]
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
    def method(cls): pass
    '''
    annotation = func.__annotations__.get('return', Parameter.empty)
    if annotation is Parameter.empty:
        return func
    checker = AnnotationChecker('return', annotation)
    def _function(*args, **kwargs):
        return checker.check(func(*args, **kwargs))
    return _wrap(_function, func)


__all__ = [
    'check_arguments',
    'check_return'
]
