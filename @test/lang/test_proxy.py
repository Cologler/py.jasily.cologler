#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import unittest

from jasily.lang.proxy import mutable, readonly


class Test(unittest.TestCase):
    def test_mutable(self):
        class A:
            pass

        a = A()
        ap = mutable(a)

        self.assertIsInstance(ap, type(a))

        with self.assertRaises(AttributeError):
            _ = ap.a
        ap.a = 1
        self.assertEqual(1, ap.a)
        with self.assertRaises(AttributeError):
            _ = a.a

        a.a = 2
        self.assertEqual(2, a.a)
        self.assertEqual(1, ap.a)
        del ap.a
        self.assertEqual(2, ap.a)
        with self.assertRaises(AttributeError):
            del ap.a

    def test_readonly(self):
        class A:
            pass

        for error_on_set in (True, False):
            a = A()
            roa = readonly(a, error_on_set=error_on_set)

            self.assertIsInstance(roa, type(a))

            with self.assertRaises(AttributeError):
                _ = roa.b
            if error_on_set:
                with self.assertRaises(AttributeError):
                    roa.b = 1
            else:
                roa.b = 1
            with self.assertRaises(AttributeError):
                _ = roa.b

            a.b = 'b'
            self.assertEqual('b', roa.b)
            if error_on_set:
                with self.assertRaises(AttributeError):
                    roa.b = 'b'
            else:
                roa.b = 'b'
            self.assertEqual('b', roa.b)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
