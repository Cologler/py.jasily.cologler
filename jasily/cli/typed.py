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
        '''get engine instance.'''
        raise NotImplementedError

    def usage(self):
        '''print usage.'''
        raise NotImplementedError

    @property
    def state(self):
        '''get session state.'''
        raise NotImplementedError


class IFile(str):
    pass


class IFolder(str):
    pass
