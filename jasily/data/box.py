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
        '''
        get whether has value or not.
        '''
        return self._value is not None

    @property
    def value(self):
        ref = self._value
        return ref[0] if ref else None

    @value.setter
    def value(self, new_val):
        self._value = (new_val, )

    def reset(self):
        self._value = None

    def get(self, default):
        '''
        get value or `default` if value is unset.
        '''
        ref = self._value
        return ref[0] if ref else default

    def load_from_dict(self, src: dict, key):
        '''
        try load value from dict.
        if key is not exists, mark as state unset.
        '''
        if key in src:
            self.value = src[key]
        else:
            self.reset()
