#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

import os

from .exceptions import InvalidOperationException
from .check import (
    check_arguments,
    check_return,
    check_callable,
    check_generic,
    check_type
)

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

# idea from https://code.activestate.com/recipes/410692/
class switch(object):
    """
    how to use `switch` ?
    ===
    for case in switch(name):
        if case('A'):
            pass
        elif case(1, 3):
            pass # for mulit-match.
        else:
            pass # for default.
    """
    def __init__(self, value):
        self._value = value
        self._exec = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if len(args) == 0:
            raise  SyntaxError('cannot match empty pattern.')
        if self._exec: # ready exec
            raise SyntaxError('cannot call match() after matched.')
        self._exec = self._value in args
        return self._exec

