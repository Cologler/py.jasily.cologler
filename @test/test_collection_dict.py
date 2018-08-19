# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.collection.comparer import IgnoreCaseStringComparer
from jasily.collection.dict import Dictionary

def test_dictionary():
    test_dict = Dictionary(IgnoreCaseStringComparer())
    test_dict['a'] = 1
    assert test_dict['A'] == 1
    assert list(test_dict) == ['a']
