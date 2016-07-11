#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

import os
import inspect

def pip_require(module_name, pip_name=None):
    '''auto call `pip install` if module not install.'''
    try:
        __import__(module_name)
    except ImportError:
        if os.system('pip install ' + pip_name or module_name) != 0:
            raise ImportError('can not found module call ' + module_name)


def type_check(value, *checkers, name=None):
    '''
    check value type (and convert if need).
    return value.

    each checker can be (type|(type)|(type, func)), func only accept 1 args.

    e.g. 1: type_check(1, str) -> raise TypeError
    e.g. 2: type_check(1, int) -> 1
    e.g. 3: type_check(1, str, int) -> 1
    e.g. 3: type_check(1, str, (int, int.__str__)) -> '1'
    '''
    assert len(checkers) > 0
    def raise_type_error(types, argname):
        raise TypeError("%s must be (%s)" % (argname, ' or '.join([x.__name__ for x in types])))
    allowed_types = []
    for checker in checkers:
        _t = None
        _c = None
        if isinstance(checker, type):
            _t = checker
        elif isinstance(checker, tuple) or isinstance(checker, list):
            if len(checker) == 1:
                _t = checker[0]
            elif len(checker) == 2:
                _t = checker[0]
                _c = checker[1]
        if _t is None:
            raise ValueError
        allowed_types.append(_t)
        if isinstance(value, _t):
            if _c is None:
                return value
            else:
                return _c(value)
    raise_type_error(allowed_types, name or 'value')

#####
# check func parameter for func annotation
#####

def __check_type(arg, tp):
    if not isinstance(arg, tp):
        raise TypeError("%s is not of type %s" % (arg, tp.__name__))

def __check_annotation(arg, a):
    if isinstance(a, type):
        return __check_type(arg, a)    
    __check_type(arg, type(a)) 
    if '__iter__' in dir(a): # annotation is some kind of tuple/list ?
        l1 = list(arg)
        l2 = list(a)
        if len(l1) != len(l2):
            if len(l1) > len(l2):
                raise ValueError(
                    'too many values to unpack (expected %s)' % len(l2))
            else:
                raise ValueError(
                    'not enough values to unpack (expected %s, got %s)' % (len(l2), len(l1)))
        for l, r in zip(l1, l2):
            __check_annotation(l, r)

def checkargs(func):
    '''check method args by annotation.'''
    def _f(*args):
        for index, arg in enumerate(inspect.getfullargspec(func)[0]):
            if arg in func.__annotations__[arg]:
                __check_annotation(args[index], func.__annotations__[arg])
        return func(*args)
    _f.__doc__ = func.__doc__
    return _f