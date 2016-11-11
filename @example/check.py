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
from jasily import (
    check_arguments,
    check_return,
    check_callable,
    check_type
)

# pylint: disable=W0612
# pylint: disable=W0613

class TestCheckMethods(unittest.TestCase):
    def test_base(self):
        @check_arguments
        def func1(arg1: str): pass
        func1('')
        with self.assertRaises(TypeError):
            func1(1)

        @check_arguments
        def func2(arg1: (str, int)): pass
        func2('')
        func2(1)
        with self.assertRaises(TypeError):
            func2(object())

    def test_callable(self):
        with self.assertRaises(InvalidOperationException):
            def func_1000(arg1, arg2):
                pass
            @check_arguments
            def func_1001(arg: func_1000):
                pass

    def test_check_arguments_3(self):
        def func_check(arg):
            return not isinstance(arg, str)
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

    def test_check_type(self):
        check_type('', str)
        check_type('', str, int)
        check_type('', float, str, int)
        check_type('', float, str, int, None)
        check_type(None, float, str, int, None)
        with self.assertRaises(TypeError):
            check_type('', int)
        with self.assertRaises(TypeError):
            check_type('', float, int)

if __name__ == '__main__':
    unittest.main()
