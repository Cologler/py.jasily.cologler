# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pytest

from jasily.oop import *

def test_final():
    class A(Final):
        pass

    with pytest.raises(TypeError):
        class B(A):
            pass

    with pytest.raises(TypeError):
        class C(A, Final):
            pass
