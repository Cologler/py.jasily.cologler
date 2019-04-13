# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pytest

from jasily.lang.props import prop, get_only

def test_prop_default():
    class SomeClass:
        @prop
        def value(self):
            pass

    obj = SomeClass()
    assert not hasattr(obj, '_value')
    with pytest.raises(AttributeError):
        _ = obj.value
    obj.value = 1
    assert hasattr(obj, '_value')
    assert obj.value == 1
    assert getattr(obj, '_value') == 1

def test_prop_all_feature():
    class SomeClass:
        @prop(field='_some_field', get=True, set=True, del_=True, default=3, types=(str, bytes))
        def value(self):
            pass

    obj = SomeClass()
    assert not hasattr(obj, '_some_field')
    assert obj.value == 3

    with pytest.raises(TypeError):
        obj.value = 1
    assert not hasattr(obj, '_some_field')
    assert obj.value == 3

    obj.value = '24'
    assert getattr(obj, '_some_field') == '24'
    assert obj.value == '24'

    del obj.value
    assert not hasattr(obj, '_some_field')
    assert obj.value == 3

def test_field_name_equals_property_name():
    class SomeClass:
        @prop(field='value')
        def value(self):
            pass

    obj = SomeClass()
    with pytest.raises(AttributeError):
        _ = obj.value

    obj.value = 1
    assert obj.value == 1

def test_get_only():
    class Any:
        value = get_only('_value')

        def __init__(self):
            self._value = 2

    assert Any().value == 2
