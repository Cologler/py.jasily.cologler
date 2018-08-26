# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from jasily.data.mapper import from_dict, to_dict

def test_simple_model():
    class Model:
        a: int

    input_data = {
        'a': 15
    }

    obj: Model = from_dict(Model, input_data)
    assert isinstance(obj, Model)

    # ensure attr not in class
    with raises(AttributeError):
        _ = Model.a
    # ensure attr in instance
    assert obj.a == input_data['a']
    assert obj.__dict__ == input_data

    assert to_dict(obj) == input_data

def test_deep_model():
    class Model1:
        f1: int

    class Model2:
        f2: Model1

    input_data = {
        'f2': {
            'f1': 1,
        }
    }

    obj: Model2 = from_dict(Model2, input_data)
    assert isinstance(obj, Model2)
    assert isinstance(obj.f2, Model1)
    assert obj.f2.f1 == 1
    assert to_dict(obj) == input_data

def test_empty_model():
    class Model:
        pass

    data = to_dict(Model())
    assert data == {}

    # should not raise:
    from_dict(Model, {})

def test_model_has_other_fields():
    class Model:
        pass

    input_data = {
        'a': 15
    }

    with raises(TypeError):
        from_dict(Model, input_data)

    # not strict mode
    obj: Model = from_dict(Model, input_data, strict=False)
    assert obj.a == 15
