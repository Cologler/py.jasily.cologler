# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pytest

from jasily.decorator.method import (
    cache,
    once, assert_once
)

def test_cache():
    time = 0

    class A:
        @cache
        def func(self):
            nonlocal time
            time += 1
            return time

    a = A()
    assert a.func() == 1
    assert a.func() == 1
    assert a.func() == 1

def test_once():
    time = 0

    class A:
        @once
        def func(self):
            nonlocal time
            time += 1
            return 100

    a = A()
    assert a.func() is None
    assert a.func() is None
    assert a.func() is None
    assert time == 1

def test_assert_once():
    time = 0

    class A:
        @assert_once
        def func(self):
            nonlocal time
            time += 1
            return 100

    a = A()
    assert a.func() is None
    with pytest.raises(AssertionError):
        a.func()
    with pytest.raises(AssertionError):
        a.func()
    assert time == 1