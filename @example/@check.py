#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily import InvalidOperationException
from jasily import check_arguments
from jasily import check_return

@check_arguments
def func1(arg1: str):
    pass

# pass
func1('')

# error
try:
    func1(1)
except TypeError:
    pass
else:
    raise AssertionError

@check_arguments
def func2(arg1: (str, int)):
    pass

# pass
func2('')
func2(1)

# error
try:
    func2(object())
except TypeError:
    pass
else:
    raise AssertionError

# replace type to accept 1 arg callable
try:
    def func_1000(arg1, arg2):
        pass
    @check_arguments
    def func_1001(arg: func_1000):
        pass
except InvalidOperationException: # too many arg
    pass
else:
    raise AssertionError

def func_check(arg):
    return not isinstance(arg, str)

@check_arguments
def func3(arg1: func_check):
    pass

# pass
func3(None)
func3(1)

# EOFError
try:
    func3('')
except TypeError:
    pass
else:
    raise AssertionError




print('test completed.')
