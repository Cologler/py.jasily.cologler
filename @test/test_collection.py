# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.collection.comparer import IgnoreCaseStringEqualityComparer
from jasily.collection.dict import Dictionary
from jasily.collection.set import HashSet

def test_dictionary():
    test_dict = Dictionary(IgnoreCaseStringEqualityComparer())
    test_dict['a'] = 1
    assert test_dict['A'] == 1
    assert len(test_dict) == 1
    assert list(test_dict) == ['a']

def test_hashset():
    test_set = HashSet(IgnoreCaseStringEqualityComparer())
    assert 'a' not in test_set
    test_set.add('A')
    assert 'a' in test_set
    assert len(test_set) == 1
    assert list(test_set) == ['A']
