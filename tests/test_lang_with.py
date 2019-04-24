# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.lang import with_it, with_objattr, with_objattrs

class SomeLock:
    def __init__(self):
        self.locked = False

    def __enter__(self):
        self.locked = True

    def __exit__(self, *args):
        self.locked = False

def test_with_it():
    lock = SomeLock()
    @with_it(lock)
    def func():
        assert lock.locked
        return 1
    assert not lock.locked
    assert func() == 1
    assert not lock.locked

def test_with_objattr():
    class X:
        def __init__(self):
            self.some_lock = SomeLock()

        @with_objattr('some_lock')
        def func(self):
            assert self.some_lock.locked
            return 1

    x = X()
    assert not x.some_lock.locked
    assert x.func() == 1
    assert not x.some_lock.locked

def test_with_objattrs():
    class X:
        def __init__(self):
            self.some_lock_1 = SomeLock()
            self.some_lock_2 = SomeLock()

        @with_objattrs('some_lock_1', 'some_lock_2')
        def func(self):
            assert self.some_lock_1.locked
            assert self.some_lock_2.locked
            return 1

    x = X()
    assert not x.some_lock_1.locked
    assert not x.some_lock_2.locked
    assert x.func() == 1
    assert not x.some_lock_1.locked
    assert not x.some_lock_2.locked
