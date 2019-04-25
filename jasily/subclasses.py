# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class SubClassMixin:
    __subclasses = {}

    def __init_subclass__(cls, *_, **_k):
        for base in cls.__mro__[:-1]:
            if issubclass(base, SubClassMixin):
                try:
                    scs = SubClassMixin.__subclasses[base]
                except KeyError:
                    scs = SubClassMixin.__subclasses.setdefault(base, [])
                scs.append(cls)

    @staticmethod
    def subclasses_of(base):
        return tuple(SubClassMixin.__subclasses[base])

    @classmethod
    def subclasses(cls):
        return SubClassMixin.subclasses_of(cls)
