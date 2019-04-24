# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.collection.comparer import StringComparer
from jasily.collection.set import HashSet

def test_hashset():
    test_set = HashSet(StringComparer.IgnoreCaseComparer)
    assert 'a' not in test_set
    test_set.add('A')
    assert 'a' in test_set
    assert len(test_set) == 1
    assert list(test_set) == ['A']
