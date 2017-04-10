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
from jasily.convert import *


class TestStringTypeConverter(unittest.TestCase):
    def test_expect_None(self):
        with self.assertRaises(ArgumentTypeException):
            StringTypeConverter().convert(None, 1)
        StringTypeConverter().convert(None, 1)


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
