#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
from jasily.exceptions import InvalidOperationException
from jasily.check import check_arguments
from jasily.check import check_return
from jasily.check import check_generic
from _test import assert_error

@check_arguments
def func1(arg1: str):
    pass

# pass
func1('')
# error
assert_error(TypeError, func1, 1)

@check_arguments
def func2(arg1: (str, int)):
    pass

# pass
func2('')
func2(1)
# error
assert_error(TypeError, func2, object())

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
# error
assert_error(TypeError, func3, '')

@check_return
def func4(a) -> (str, None):
    return a or 1

# pass
func4('2')
# error
assert_error(TypeError, func4, None)
assert_error(TypeError, func4, 1)

check_generic([], typing.List[int])
check_generic([1], typing.List[int])
assert_error(TypeError, check_generic, ['2'], typing.List[int])

check_generic({}, typing.Dict[int, str])
check_generic({1: ''}, typing.Dict[int, str])
assert_error(TypeError, check_generic, {1: 2}, typing.Dict[int, str])
assert_error(TypeError, check_generic, {'': '2'}, typing.Dict[int, str])

check_generic((1, ''), typing.Tuple[int, str])
assert_error(TypeError, check_generic, (1, ), typing.Tuple[int, str])

check_generic((1, ['']), typing.Tuple[int, typing.List[str]])

print('test completed.')
