# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.data.box import Box

def assert_has_value(box: Box, value):
    assert box.has_value is True
    assert box.value == value

def assert_no_value(box: Box):
    assert box.has_value is False
    assert box.value is None

def test_box_init_state():
    box = Box()
    assert_no_value(box)

def test_box_set_value():
    box = Box()
    # set value
    box.value = 1
    assert_has_value(box, 1)
    # reset value
    box.reset()
    assert_no_value(box)

def test_box_get():
    box = Box()
    assert box.get(3) == 3
    box.value = 1
    assert box.get(3) == 1
    box.reset()
    assert box.get(4) == 4

def test_box_load_from_dict():
    box = Box()
    box.load_from_dict({'a': 1}, 'a')
    assert_has_value(box, 1)
    box.load_from_dict({'a': 1}, 'b')
    assert_no_value(box)
