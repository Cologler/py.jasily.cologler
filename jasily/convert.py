#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

from . import check_arguments
from .exceptions import ArgumentTypeException

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
        conv_func = self._to.get(type)
        if conv_func:
            try:
                return conv_func(value)
            except ValueError:
                raise ConvertError
        else:
            raise NotImplementedError

    def to_str(self, value) -> str:
        return str(value)

    @classmethod
    @check_arguments
    def from_type(cls, source_type: type):
        '''
        [Thread-Safely]
        from source type create a defined converter.
        '''
        source = cls._cached
        ret = source.get(source_type)
        if ret != None:
            return ret
        if source_type == str:
            ret = StringConverter()
            # copy-on-write
            source = source.copy()
            source[source_type] = ret
            cls._cached = source
            return ret
        raise NotImplementedError

class StringConverter(Converter):
    def __init__(self):
        super().__init__(str)

    def to_int(self, value: str) -> int:
        return int(value)

    def to_float(self, value: str) -> float:
        return float(value)

    def to_bool(self, value: str) -> bool:
        lower = value.lower()
        if lower == 'true':
            return True
        elif lower == 'false':
            return False
        raise ConvertError


class TypeConvertException(Exception):
    def __init__(self, value, except_type,
                 error=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value
        self._error = error
        self._except_type = except_type


class TypeConverter:
    G_TYPE = type

    def __init__(self, from_type):
        self._type = from_type
        self._convmap = {}
        for attr in [attr for attr in dir(self) if attr.startswith('to_')]:
            func = getattr(self, attr)
            ret = func.__annotations__.get('return')
            if isinstance(ret, type):
                self._convmap[ret] = func
        if self._convmap.get(self._type) is None:
            self._convmap[self._type] = self._to_self

    def _to_self(self, value):
        return value

    def convert(self, type, value):
        '''raise `TypeConvertException` is convert failed.'''
        if type is None:
            raise ArgumentTypeException(self.G_TYPE, None)
        func = self._convmap.get(type)
        if func is None:
            raise NotImplementedError
        try:
            return func(value)
        except Exception as err:
            raise TypeConvertException(value, type, err)


class StringTypeConverter(TypeConverter):
    def __init__(self):
        super().__init__(str)

    def to_int(self, value: str) -> int:
        return int(value)

    def to_float(self, value: str) -> float:
        return float(value)

    def to_bool(self, value: str) -> bool:
        lower = value.lower()
        if lower == 'true':
            return True
        elif lower == 'false':
            return False
        raise ConvertError
