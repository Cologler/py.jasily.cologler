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

from jasily.cli.args import *

class TestConstant(unittest.TestCase):
    def test_ENGLISG(self):
        self.assertEqual(ENGLISG, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.assertEqual(len(ENGLISG), 26 * 2)


class TestArgumentParser(unittest.TestCase):
    def _assert_result_common(self, result: tuple):
        for idx, item in enumerate(result):
            assert isinstance(item, ArgumentValue)
            self.assertEqual(idx, item.index)

    def test_example_1(self):
        argv = [
            'a1', 'a2', 'a3',
            '-FLAG', # -> 'F', 'L', 'A', 'G' 4 flag.
            '--flag080',
            '--k15', 'v11', '--k25', 'v27', '--k36', '\\--v36',
            '--k46:v24', '--k53=v75',
            '--flag180', '--flag050', '--flag999'
        ]
        parser = ArgumentParser(argv)
        result = parser.resolve()
        self._assert_result_common(result)
        self.assertEqual(16, len(result))
        self.assertEqual(tuple(result[0 ]), (None, 'a1'))
        self.assertEqual(tuple(result[1 ]), (None, 'a2'))
        self.assertEqual(tuple(result[2 ]), (None, 'a3'))
        self.assertEqual(tuple(result[3 ]), ('F', None))
        self.assertEqual(tuple(result[4 ]), ('L', None))
        self.assertEqual(tuple(result[5 ]), ('A', None))
        self.assertEqual(tuple(result[6 ]), ('G', None))
        self.assertEqual(tuple(result[7 ]), ('flag080', None))
        self.assertEqual(tuple(result[8 ]), ('k15', 'v11'))
        self.assertEqual(tuple(result[9 ]), ('k25', 'v27'))
        self.assertEqual(tuple(result[10]), ('k36', '--v36'))
        self.assertEqual(tuple(result[11]), ('k46', 'v24'))
        self.assertEqual(tuple(result[12]), ('k53', 'v75'))
        self.assertEqual(tuple(result[13]), ('flag180', None))
        self.assertEqual(tuple(result[14]), ('flag050', None))
        self.assertEqual(tuple(result[15]), ('flag999', None))

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
