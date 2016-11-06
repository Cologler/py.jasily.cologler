#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

from . import check_arguments
from .descriptors import thread_not_safely

class ConvertError(Exception):
    pass

class Converter:
    _cached = {}
    def __init__(self, source_type):
        self._type = source_type
        self._to = {}
        attrs = [attr for attr in dir(self) if attr.startswith('to_')]
        for attr in attrs:
            func = getattr(self, attr)
            ret_val = func.__annotations__.get('return')
            if isinstance(ret_val, type):
                self._to[ret_val] = func

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
    @thread_not_safely
    @check_arguments
    def from_type(cls, source_type: type):
        '''from source type create a defined converter.'''
        ret = cls._cached.get(source_type)
        if ret != None:
            return ret
        if source_type == str:
            ret = StringConverter()
            cls._cached[source_type] = ret
            return ret
        raise NotImplementedError

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
