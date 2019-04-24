# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.subclasses import BaseClass

def test_subclass():
    class A(BaseClass):
        pass

    assert A.subclasses() == (A, )

def test_subclass_subsubclass():
    class A(BaseClass):
        pass

    class B(A):
        pass

    assert A.subclasses() == (A, B)
    assert B.subclasses() == (B,  )
