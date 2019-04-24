# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.threads import Counter

def test_counter():
    counter = Counter(3)
    assert counter.value == 3
    with counter:
        assert counter.value == 4
    assert counter.value == 3
    assert counter.incr() == 4
    assert counter.value == 4
    assert counter.decr() == 3
    assert counter.value == 3
