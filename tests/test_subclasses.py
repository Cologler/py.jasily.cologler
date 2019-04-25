# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.subclasses import SubClassMixin

def test_subclass():
    class A(SubClassMixin):
        pass

    assert A.subclasses() == (A, )

def test_subclass_subsubclass():
    class A(SubClassMixin):
        pass

    class B(A):
        pass

    assert A.subclasses() == (A, B)
    assert B.subclasses() == (B,  )
