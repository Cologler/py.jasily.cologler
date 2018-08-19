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

from jasily.objects import *


class TestUInt(unittest.TestCase):
    def test_ctor(self):
        with self.assertRaises(ValueError):
            uint(-2)
        with self.assertRaises(ValueError):
            uint(-1)
        uint(0)
        uint(1)

    def test_eq(self):
        value = uint(3)
        self.assertEqual(3, value)

    def test_int(self):
        value = int(uint(3))
        self.assertIsInstance(value, int)
        self.assertEqual(3, value)


class TestSet(unittest.TestCase):
    def test_add(self):
        s = Set()
        self.assertEqual(True, s.add(5))
        self.assertEqual(False, s.add(5))
        self.assertEqual(False, s.add(5))


class TestChar(unittest.TestCase):
    def test_ctor(self):
        with self.assertRaises(ValueError):
            Char(-5)
        with self.assertRaises(ValueError):
            Char('-5')

    def __assert(self, value):
        ch = Char(value)
        if isinstance(value, str):
            ch = str(ch)
        elif isinstance(value, int):
            ch = int(ch)
        self.assertEqual(value, ch)

    def test_str(self):
        self.__assert('5')
        self.__assert('s')
        self.__assert('S')
        self.__assert('S')

    def test_int(self):
        self.__assert(5)
        self.__assert(10)
        self.__assert(15)
        self.__assert(20)


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

