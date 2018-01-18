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

from jasily.data.prop import cache, getonly_property

class Test(unittest.TestCase):

    def test_getonly_property(self):
        class A:
            @getonly_property
            def name(self):
                return 'name'

        self.assertEqual(A().name, 'name')

    def test_getonly_property_attrs(self):
        class A:
            @property
            def a(self):
                '''doc for a().'''
                pass

        class B:
            @getonly_property
            def a(self):
                '''doc for a().'''
                pass

        self.assertEqual(A.a.__doc__, B.a.__doc__)

    def test_cache(self):
        class A:
            def __init__(self):
                self._inc_a = 0
                self._inc_b = 0

            @cache
            @property
            def a(self):
                self._inc_a += 1
                return self._inc_a

            @cache
            @property
            def b(self):
                self._inc_b += 1
                return self._inc_b

        ins = A()
        self.assertEqual(1, ins.a)
        self.assertEqual(1, ins.a)
        self.assertEqual(1, ins.a)
        self.assertEqual(1, ins.b)
        self.assertEqual(1, ins.b)
        self.assertEqual(1, ins.b)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
