#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

from . import check_annotation

class ConvertError(Exception):
    pass

 

class Converter:
    _cached = {}

    def __init__(self, tp):
        self._type = tp
        self._to = {}
        attrs = [attr for attr in dir(self) if attr.startswith('to_')]
        for attr in attrs:
            ret_val = getattr(self, attr).__annotations__.get('return')
            print(attr)
            print(type(ret_val))
            assert isinstance(ret_val, type)
            self._to[ret_val] = getattr(self, attr)
    
    def _to_self(self, value):
        return value

    def to(self, type, value):
        '''
        raise ConvertError if convert error.
        raise NotImplementedError if not support convert
        '''
        if type == self._type:
            return self._to_self(value)
        converter = self._to.get(type)
        if converter:
            return converter(value)
        else:
            raise NotImplementedError

    @classmethod
    @check_annotation
    def from_type(cls, tp: type):
        ret = cls._cached.get(tp)
        if not ret is None:
            return ret
        if tp == str:
            ret = StringConverter()
            cls._cached[tp] = ret
            return ret

class StringConverter(Converter):
    def __init__(self):
        super().__init__(str)

    def to_int(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ConvertError

    def to_float(self, value: str)-> float:
        try:
            return float(value)
        except ValueError:
            raise ConvertError