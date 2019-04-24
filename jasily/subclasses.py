# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class BaseClass:
    __subclasses = {}

    def __init_subclass__(cls, *_, **_k):
        for base in cls.__mro__[:-1]:
            if issubclass(base, BaseClass):
                try:
                    scs = BaseClass.__subclasses[base]
                except KeyError:
                    scs = BaseClass.__subclasses.setdefault(base, [])
                scs.append(cls)

    @staticmethod
    def subclasses_of(base):
        return tuple(BaseClass.__subclasses[base])

    @classmethod
    def subclasses(cls):
        return BaseClass.subclasses_of(cls)
