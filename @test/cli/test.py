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

from jasily.cli import *

class TestClass1:
    @property
    def p(self):
        return 'property'

    def m(self):
        return 'method'

    @classmethod
    def cm(cls):
        return 'classmethod'

    @staticmethod
    def sm():
        return 'staticmethod'


class TestEngine(unittest.TestCase):
    def test_simple_object(self):
        # float
        self.assertEqual(3.3, fire(3.3).execute([]))
        # int
        self.assertEqual(3, fire(3).execute([]))
        # str
        self.assertEqual('3', fire('3').execute([]))
        # dict
        self.assertEqual('3', fire({'2': '3'}).execute(['2']))
        self.assertEqual(5, fire({'2': '3', '4': 5}).execute(['4']))
        # tuple
        self.assertEqual(1, fire((1, 2)).execute(['0']))
        self.assertEqual(2, fire((1, 2)).execute(['1']))
        with self.assertRaises(ParameterException):
            self.assertEqual(None, fire((1, 2)).execute(['\\-1'], True))
        # list
        self.assertEqual(1, fire([1, 2]).execute(['0']))
        self.assertEqual(2, fire([1, 2]).execute(['1']))

    def test_sclass_NO_args(self):
        e = fire(TestClass1)
        self.assertEqual('property', e.execute(['p']))
        self.assertEqual('method', e.execute(['m']))
        self.assertEqual('classmethod', e.execute(['cm']))
        self.assertEqual('staticmethod', e.execute(['sm']))


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