#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

LIST_ARGS = (list, tuple)

class IEngine:
    def execute(self, argv):
        raise NotImplementedError


class ISession:
    @property
    def engine(self) -> IEngine:
        raise NotImplementedError


def maptype(s: ISession):
    typedmap = {}
    typedmap[IEngine] = s.engine
    typedmap[ISession] = s
    return typedmap


class IFile(str):
    pass


class IFolder(str):
    pass
