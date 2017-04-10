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
            UInt(-2)
        with self.assertRaises(ValueError):
            UInt(-1)
        UInt(0)
        UInt(1)

    def test_eq(self):
        value = UInt(3)
        self.assertEqual(3, value)

    def test_int(self):
        value = int(UInt(3))
        self.assertIsInstance(value, int)
        self.assertEqual(3, value)


class TestSet(unittest.TestCase):
    def test_add(self):
        s = Set()
        self.assertEqual(True, s.add(5))
        self.assertEqual(False, s.add(5))
        self.assertEqual(False, s.add(5))


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

