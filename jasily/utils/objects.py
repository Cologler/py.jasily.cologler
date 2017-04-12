#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from ..exceptions import InvalidOperationException


class Freezable:
    __FREEZABLE_FLAG = '__JASILY_FREEZABLE_IS_FREEZED__'

    '''provide a freezable check base class.'''
    def freeze(self):
        '''freeze object.'''
        setattr(self, Freezable.__FREEZABLE_FLAG, True)

    @property
    def is_freezed(self):
        '''check if freezed.'''
        return getattr(self, Freezable.__FREEZABLE_FLAG, False)

    def raise_if_freezed(self):
        '''raise `InvalidOperationException` if is freezed.'''
        if self.is_freezed:
            name = type(self).__name__
            raise InvalidOperationException('obj {name} is freezed.'.format(name=name))

