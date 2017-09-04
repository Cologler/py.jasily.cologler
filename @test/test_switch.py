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
from jasily import switch


class Test(unittest.TestCase):
    def test_switch_chain(self):
        self.assertEqual('A', switch(1).case('A', 1).case('B', 2, 4).default('3').end())
        self.assertEqual('B', switch(2).case('A', 1).case('B', 2, 4).default('3').end())
        self.assertEqual('3', switch(3).case('A', 1).case('B', 2, 4).default('3').end())
        self.assertEqual('B', switch(4).case('A', 1).case('B', 2, 4).default('3').end())
        self.assertEqual('3', switch(5).case('A', 1).case('B', 2, 4).default('3').end())

    def test_switch(self):
        def switch_result(value):
            for case in switch(value):
                if case(1):
                    return 1
                elif case(2):
                    return 2
                else:
                    return 3
        self.assertEqual(switch_result(1), 1)
        self.assertEqual(switch_result(2), 2)
        self.assertEqual(switch_result(4), 3)


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
