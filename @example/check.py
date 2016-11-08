#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import unittest
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

class TestCheckMethods(unittest.TestCase):

    def test_check_arguments_3(self):
        @check_arguments
        def func(arg1: func_check):
            pass
        func(None)
        func(1)
        with self.assertRaises(TypeError):
            func('')

    def test_check_arguments_4(self):
        @check_arguments
        def func(arg1, arg2: str=None):
            pass
        func(3)

    def test_check_return(self):
        @check_return
        def func(a) -> (str, None):
            return a or 1
        func('2')
        with self.assertRaises(TypeError):
            func(None)
        with self.assertRaises(TypeError):
            func(1)

    def test_check_generic(self):
        check_generic([], typing.List[int])
        check_generic([1], typing.List[int])
        check_generic({}, typing.Dict[int, str])
        check_generic({1: ''}, typing.Dict[int, str])
        check_generic((1, ''), typing.Tuple[int, str])
        check_generic((1, ['']), typing.Tuple[int, typing.List[str]])
        with self.assertRaises(TypeError):
            check_generic(['2'], typing.List[int])
        with self.assertRaises(TypeError):
            check_generic({1: 2}, typing.Dict[int, str])
        with self.assertRaises(TypeError):
            check_generic({'': '2'}, typing.Dict[int, str])
        with self.assertRaises(TypeError):
            check_generic((1, ), typing.Tuple[int, str])

if __name__ == '__main__':
    unittest.main()
