#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import unittest
from jasily.dependencyinjection import (TypeNotFoundError, FunctionInvoker)
from _test import assert_error


def func1(abc: str):
    return abc

class TestFunc1(unittest.TestCase):
    def test_default(self):
        invoker = FunctionInvoker()
        invoker.provide_object('4')
        self.assertEqual(invoker.invoke(func1), '4')

    def test_8(self):
        invoker = FunctionInvoker()
        invoker.provide_object('4')
        self.assertEqual(invoker.invoke(func1), '4')

    def test_2(self):
        invoker = FunctionInvoker()
        invoker.provide_object('4')
        invoker.provide_object('5')
        self.assertEqual(invoker.invoke(func1), '5')

    def test_3(self):
        invoker = FunctionInvoker()
        invoker.provide_object('4', provide_name="abc")
        invoker.provide_object('5')
        self.assertEqual(invoker.invoke(func1), '4')

    def test_4(self):
        invoker = FunctionInvoker()
        invoker.provide_object('4', provide_name="abc")
        invoker.provide_object('5')
        invoker2 = invoker.create_transient()
        invoker2.provide_object('6')
        self.assertEqual(invoker.invoke(func1), '4')
        self.assertEqual(invoker2.invoke(func1), '4') # because match name and type, so return '4'
        invoker3 = invoker.create_transient()
        invoker3.provide_object('7', provide_name="abc")
        self.assertEqual(invoker.invoke(func1), '4')
        self.assertEqual(invoker2.invoke(func1), '4')
        self.assertEqual(invoker3.invoke(func1), '7')


def func2(abce):
    return abce

class TestFunc2(unittest.TestCase):
    def test_2(self):
        invoker = FunctionInvoker()
        invoker.provide_object('5')
        with self.assertRaises(TypeNotFoundError):
            invoker.invoke(func2) # abc has no type
        invoker.provide_object(8, provide_name='abce')
        self.assertEqual(invoker.invoke(func2), 8)

def func3(abc: (int, str)):
    return abc

class TestFunc3(unittest.TestCase):
    def test_3(self):
        invoker = FunctionInvoker()
        invoker.provide_object(3)
        self.assertEqual(invoker.invoke(func3), 3)

        invoker2 = FunctionInvoker()
        invoker2.provide_object(3)
        invoker2.provide_object('4')
        self.assertEqual(invoker2.invoke(func3), 3) # should match first type (int)

        invoker3 = FunctionInvoker()
        invoker3.provide_object('4')
        invoker3.provide_object(3)
        self.assertEqual(invoker3.invoke(func3), 3) # should match first type (int)

        invoker4 = FunctionInvoker()
        invoker4.provide_object('4', provide_name='abc')
        invoker4.provide_object(3)
        self.assertEqual(invoker4.invoke(func3), '4')

def func4(ab: list):
    return ab

class A:
    def __init__(self, arg: list):
        self.arg = arg

    def test_dict_1(self, x: list) -> dict:
        return {}

    def test_dict_2(self, d: dict):
        return d

def func5(ab: A):
    return ab

class TestFunc4And5(unittest.TestCase):
    def test_create_instance(self):
        invoker = FunctionInvoker()
        invoker.provide_callable(lambda : [], provide_type=list)
        self.assertIsInstance(invoker.invoke(func4), list)

    def test_create_instance_miss_type(self):
        with self.assertRaises(TypeError):
            invoker = FunctionInvoker()
            invoker.provide_callable(lambda : [])

    def test_create_instance_deep(self):
        invoker = FunctionInvoker()
        invoker.provide_callable(lambda : [], provide_type=list)
        invoker.provide_callable(A, provide_type=A, invoker=invoker)
        self.assertIsInstance(invoker.invoke(func5), A)

    def test_create_instance_deep_miss_A_arg(self):
        invoker = FunctionInvoker()
        invoker.provide_callable(A, provide_type=A)
        with self.assertRaises(TypeError):
            self.assertIsInstance(invoker.invoke(func5), A)

    def test_instance_method(self):
        invoker = FunctionInvoker()
        a = A([])
        invoker.provide_callable(lambda : [], provide_type=list)
        invoker.provide_callable(a.test_dict_1, invoker=invoker)
        self.assertIsInstance(invoker.invoke(a.test_dict_2), dict)
        print(invoker)

if __name__ == '__main__':
    unittest.main()
