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


class Set(set):
    def add(self, v):
        size = len(self)
        set.add(self, v)
        return len(self) > size


class Char:
    def __init__(self, ch: (str, int)):
        self._value_int: int = None
        self._value_str: str = None
        if isinstance(ch, Char):
            self._value_int = ch._value_int
            self._value_str = ch._value_int
        elif isinstance(ch, str):
            if len(ch) != 1:
                raise ValueError
            self._value_str = ch
            self._value_int = ord(ch)
        elif isinstance(ch, int):
            self._value_int = ch
            self._value_str = chr(ch)
        else:
            raise ValueError

    def __int__(self):
        return self._value_int

    def __str__(self):
        return self._value_str

    def __hash__(self):
        return hash(self._value_int)

    def __eq__(self, value):
        if isinstance(value, Char):
            return self._value_int == value._value_int
        elif isinstance(value, str):
            return str(self) == value
        elif isinstance(value, int):
            return int(self) == value
        else:
            return NotImplemented
