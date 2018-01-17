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
from jasily.cli.exceptions import UserInputException


class TestEngine(unittest.TestCase):
    def test_simple_object(self):
        # float
        self.assertEqual(3.3, fire(3.3, []))
        # int
        self.assertEqual(3, fire(3, []))
        # str
        self.assertEqual('3', fire('3', []))
        # dict
        self.assertEqual('3', fire({'2': '3'}, ['2']))
        self.assertEqual(5, fire({'2': '3', '4': 5}, ['4']))
        # tuple
        self.assertEqual(1, fire((1, 2), ['0']))
        self.assertEqual(2, fire((1, 2), ['1']))
        with self.assertRaises(UserInputException):
            self.assertEqual(None, fire((1, 2), ['\\-1'], keep_error=True))
        # list
        self.assertEqual(1, fire([1, 2], ['0']))
        self.assertEqual(2, fire([1, 2], ['1']))
        with self.assertRaises(UserInputException):
            self.assertEqual(2, fire([1, 2], ['1', '0'], keep_error=True))

    def test_single_class_NO_args(self):
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
        e = EngineBuilder().add(TestClass1).build()
        self.assertEqual('property', e.execute(['p']))
        self.assertEqual('method', e.execute(['m']))
        self.assertEqual('classmethod', e.execute(['cm']))
        self.assertEqual('staticmethod', e.execute(['sm']))

    def test_single_class_args(self):
        class TestClass1:
            def args_list(self, obj: list):
                return obj

            def args_tuple(self, obj: tuple):
                return obj

        e = EngineBuilder().add(TestClass1).build()
        with self.assertRaises(UserInputException):
            e.execute(['args-list'], True)
        self.assertEqual(['324', '185'], e.execute(['args-list', '324', '185']))
        self.assertEqual(('324', '185'), e.execute(['args-tuple', '324', '185']))


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
