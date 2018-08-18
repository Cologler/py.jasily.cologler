#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class Box:
    '''
    `Box` is a class to describe is a field has value or not.

    This is useful for some field which vaild value canbe `None` or other any special value.
    '''

    def __init__(self):
        self._value = None # `None` or tuple.

    @property
    def has_value(self):
        return self._value is not None

    @property
    def value(self):
        return self._value[0] if self._value else None

    @value.setter
    def value(self, new_val):
        self._value = (new_val, )

    def reset(self):
        self._value = None

    def get(self, default):
        return self._value[0] if self._value else default

    def load_from_dict(self, src: dict, key):
        if key in src:
            self.value = src[key]
        else:
            self.reset()
