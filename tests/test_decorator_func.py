# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pytest

from jasily.decorator.func import (
    once, assert_once
)

def test_once():
    time = 0

    @once
    def func():
        nonlocal time
        time += 1
        return 100

    assert func() is None
    assert func() is None
    assert func() is None
    assert time == 1

def test_assert_once():
    time = 0

    @assert_once
    def func():
        nonlocal time
        time += 1
        return 100

    assert func() is None
    with pytest.raises(AssertionError):
        func()
    with pytest.raises(AssertionError):
        func()
    assert time == 1
