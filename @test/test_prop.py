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
from jasily import prop

# pylint: disable=E1101, W0212
class Class1:
    @prop
    def prop1(self):
        pass

    @property
    def prop2(self):
        return self._prop1

    @prop(field='_prop_03')
    def prop3(self):
        pass

    @prop(field='__prop_04')
    def prop4(self):
        pass


class Test(unittest.TestCase):
    def test_error_message(self):
        obj = Class1()
        try:
            r = obj.prop1
        except AttributeError as err:
            msg1 = str(err)
        try:
            r = obj.prop2
        except AttributeError as err:
            msg2 = str(err)
        self.assertEqual(msg1, msg2)

    def test_getter(self):
        obj = Class1()
        obj._prop1 = 1
        self.assertEqual(obj.prop1, obj.prop2)

    def test_setter(self):
        obj = Class1()
        obj.prop1 = 1
        self.assertEqual(obj.prop1, obj.prop2)

    def test_field(self):
        obj = Class1()
        obj.prop3 = 1
        self.assertEqual(1, obj.prop3)
        self.assertEqual(1, obj._prop_03)

    def test_private(self):
        obj = Class1()
        obj.prop4 = 1
        self.assertEqual(1, obj.prop4)


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
