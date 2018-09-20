#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import unittest

from jasily.exceptions import ArgumentTypeException
from jasily.objects import uint
from jasily.convert import *


class TestStringTypeConverter(unittest.TestCase):
    Converter = StringTypeConverter()

    def test_expect_NOT_type(self):
        with self.assertRaises(TypeError):
            self.Converter.convert(None, 1)
        with self.assertRaises(TypeError):
            self.Converter.convert('None', 1)

    def test_expect_NOT_value(self):
        with self.assertRaises(TypeError):
            self.Converter.convert(str, 1)

    def test_expect_NOT_support(self):
        with self.assertRaises(TypeNotSupportException):
            self.Converter.convert(object, '1')

    def test_convert_bool(self):
        self.assertEqual(True, self.Converter.convert(bool, 'true'))
        self.assertEqual(True, self.Converter.convert(bool, '1'))
        self.assertEqual(False, self.Converter.convert(bool, 'false'))
        self.assertEqual(False, self.Converter.convert(bool, '0'))
        with self.assertRaises(TypeConvertException):
            self.assertEqual(False, self.Converter.convert(bool, '2'))

    def test_convert_int(self):
        self.assertEqual(1, self.Converter.convert(int, '1'))
        self.assertEqual(-1, self.Converter.convert(int, '-1'))
        with self.assertRaises(TypeConvertException):
            self.assertEqual(int(1.1), self.Converter.convert(int, '1.1'))

    def test_convert_uint(self):
        self.assertEqual(1, self.Converter.convert(uint, '1'))
        with self.assertRaises(TypeConvertException):
            self.assertEqual(-1, self.Converter.convert(uint, '-1'))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
