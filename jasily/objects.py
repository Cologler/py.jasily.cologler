#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# the missing
# ----------

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


class Key(object):
    '''a object key to support sort (in `dir`).'''
    __slots__ = ()

    def __gt__(self, other):
        if type(other) is Key:
            return id(self) > id(other)
        return True

    def __lt__(self, other):
        if type(other) is Key:
            return id(self) < id(other)
        return False
