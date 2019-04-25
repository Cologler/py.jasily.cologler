# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class FinalMixin:
    '''
    a mixin class that use for prevent inherit.
    '''

    def __init_subclass__(cls, *args, **kwargs):
        if Final not in cls.__bases__:
            raise TypeError('unable to inherit final class')

        for base in cls.__bases__:
            if Final in base.__bases__:
                raise TypeError('unable to inherit final class')


Sealed = SealedMixin = Final = FinalMixin
