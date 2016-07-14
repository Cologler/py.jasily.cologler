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

def _check_type(name, value, tp,
        raise_error=True):
    if value is None and tp is None:
        return True
    if isinstance(value, tp):
        return True
    if raise_error:
        n = '/'.join([x.__name__ for x in tp]) if isinstance(tp, tuple) else tp.__name__
        v = value
        raise TypeError("%s type error (expected %s, got %s)" % (
            name, n, repr(v)))
    else:
        return False

def check_annotation(func):
    '''
    check method args by annotation.
    accept:
        func(arg: str)
        func(arg: (str, int)) # or
        func(arg: None)
    not-accept:
        func(arg: (None, )) # None in tuple
    same as parameter and return value.
    '''
    def _f(*args):
        for index, arg in enumerate(inspect.getfullargspec(func)[0]):
            if arg in func.__annotations__:
                _check_type(arg, args[index], func.__annotations__[arg])
        ret = func(*args)
        if 'return' in func.__annotations__:
            _check_type('return value', ret, func.__annotations__['return'])
        return ret
    _f.__doc__ = func.__doc__
    return _f
    
# idea from https://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self._value = value
        self._exec = False
        self._pass_default = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self._pass_default:
            raise SyntaxError('cannot call cass() after default()')
        if self._exec: # ready exec
            return False
        if args: #case        
            if self._value in args:
                self._exec = True                
        else: #default
            self._pass_default = True
            self._exec = True 
        return self._exec
