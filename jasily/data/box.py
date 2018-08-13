#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class Box:
    def __init__(self):
        self._has_value = False
        self._value = None

    @property
    def has_value(self):
        return self._has_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        self._value = new_val
        self._has_value = True

    def reset(self):
        self._has_value = False
        self._value = None

    def get(self, default):
        if self._has_value:
            return self._value
        return default

    def load_from_dict(self, src: dict, key):
        if key in src:
            self._value = src[key]
            self._has_value = True
        else:
            self._value = None
            self._has_value = False
