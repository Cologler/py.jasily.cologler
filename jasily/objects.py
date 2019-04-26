#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# the missing
# ----------

import functools

class uint(int):
    '''
    the unsigned integer.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__() # object.__init__() takes no arguments
        if self < 0:
            raise ValueError(f'uint cannot less then zero.')

UInt = uint


class char(str):
    def __new__(cls, ch):
        if isinstance(ch, int):
            ch = chr(ch)

        if isinstance(ch, str):
            if len(ch) != 1:
                raise ValueError(f'too many char')
            return str.__new__(cls, ch)

        raise ValueError

    def ord(self):
        return ord(self[0])

Char = char


@functools.total_ordering
class Key(object):
    '''a object key to support sort (in `dir`).'''
    __slots__ = ('_name')

    def __init__(self, name: str=''):
        self._name = str(name)

    def __repr__(self):
        return f'Key({self._name})'

    def __gt__(self, other):
        if isinstance(other, Key):
            # only compare with type Key
            return id(self) > id(other)
        return True

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, value):
        return super().__eq__(value)
