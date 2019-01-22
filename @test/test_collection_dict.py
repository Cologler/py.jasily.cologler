# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.collection.comparer import StringComparer
from jasily.collection.dict import (
    Dictionary
)

def test_dictionary():
    test_dict = Dictionary(StringComparer.IgnoreCaseComparer)
    test_dict['a'] = 1
    assert test_dict['A'] == 1
    assert len(test_dict) == 1
    assert list(test_dict) == ['a']
