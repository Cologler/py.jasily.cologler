#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

from .exceptions import BaseException, ArgumentTypeException
from .objects import uint


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

    def to(self, type_, value):
        '''
        raise ConvertError if convert error.
        raise NotImplementedError if not support convert
        '''
        if type_ == self._type:
            return self._to_self(value)
        conv_func = self._to.get(type_)
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
    def from_type(cls, source_type: type):
        '''
        [Thread-Safely]
        from source type create a defined converter.
        '''
        source = cls._cached
        ret = source.get(source_type)
        if ret:
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


class TypeNotSupportException(BaseException):
    def __init__(self, from_type, except_type,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._from_type = from_type
        self._except_type = except_type

    def _build_str_core(self):
        f = self._from_type.__name__
        t = self._except_type.__name__
        return 'currently is not support convert from %s to %s' % (f, t)


class TypeConvertException(BaseException):
    def __init__(self, value, except_type,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value
        self._except_type = except_type

    def _build_str_core(self):
        from .utils import jrepr
        valtype = jrepr(self._value)
        return 'cannot convert from <%s> to <%s>' % (valtype, self._except_type.__name__)


class TypeConverter:
    def __init__(self, from_type):
        if not isinstance(from_type, type):
            raise TypeError

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

    def can_convert_type(self, type_):
        func = self._convmap.get(type_)
        return func is not None

    def convert(self, type_, value):
        '''
        raise `TypeNotSupportException` is cannot convert;\n
        raise `TypeConvertException` is convert failed;
        '''
        if not isinstance(type_, type):
            raise TypeError
        if not isinstance(value, self._type):
            raise TypeError

        func = self._convmap.get(type_)
        if func is None:
            raise TypeNotSupportException(self._type, type_)
        try:
            return func(value)
        except TypeConvertException:
            raise
        except Exception as err:
            raise TypeConvertException(value, type_, internal_error=err)


class StringTypeConverter(TypeConverter):
    def __init__(self):
        super().__init__(str)

    def to_uint(self, value: str) -> uint:
        return uint(self.to_int(value))

    def to_int(self, value: str) -> int:
        if '.' in value:
            raise TypeConvertException(value, int)
        return int(value)

    def to_float(self, value: str) -> float:
        return float(value)

    def to_bool(self, value: str) -> bool:
        lower = value.lower()
        if lower == 'true' or lower == '1':
            return True
        elif lower == 'false' or lower == '0':
            return False
        raise TypeConvertException(value, bool)
