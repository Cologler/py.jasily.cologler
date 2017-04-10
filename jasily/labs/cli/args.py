#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from inspect import Parameter
from ...exceptions import ApiNotSupportException, ArgumentValueException
from ...convert import StringTypeConverter


'''
arguments kinds:
* value         - sorted argument
* -flag         - single-char flag, allow (-aQu) equals (-a -Q -u)
* --flag        - mulit-chars flag (when next is not value.)
* --key value   - keyword arguments
* --key=value   - keyword arguments
* --key:value   - keyword arguments
* If want to use value `-15`, add `\` before. value always ignore first `\` char.
'''

ENGLISG = 'qwertyuiopasdfghjklzxcvbnm'
ENGLISG += ENGLISG.upper()

class ArgumentParser:
    NAME_FIRST_CHARS = ENGLISG + '_-'
    NAME_CHARS = NAME_FIRST_CHARS + '0123456789'

    def __init__(self, args: list):
        self._raw_args = args
        self._args = args.copy()
        self._result = []
        self._spliters = ('=', ':')

    def __check_argument_name(self, name: str):
        if len(name) == 0:
            raise NotImplementedError
        if name[0] not in self.NAME_FIRST_CHARS:
            raise NotImplementedError(name)
        for c in name[1:]:
            if c not in self.NAME_CHARS:
                raise NotImplementedError(name)

    def __create(self, name, value):
        if name != None:
            self.__check_argument_name(name)
        return ArgumentValue(self.__index(), name=name, value=value)

    def __index(self):
        return len(self._result)

    def __raise_unknown_name(self, value):
        msg = 'unknown argument name in <{value}> (pos %s)' % (len(self._raw_args) - len(self._args))
        raise ArgumentValueException(value, msg)

    def __get_spliter(self, k):
        spliter = None
        for sp in self._spliters:
            if sp not in k:
                continue
            if spliter != None:
                raise NotImplementedError # wtf
            spliter = sp
        return spliter

    def __resolve_argument(self):
        k = self._args.pop(0)
        return self.__parse_argument(k)

    def __parse_argument(self, k):
        if k.startswith('--'):
            if len(k) == 2:
                return self.__raise_unknown_name(k)
            k = k[2:]
            sp = self.__get_spliter(k)
            if sp is None:
                n = k
                if len(self._args) > 0 and not self._args[0].startswith('-'):
                    v = self._args.pop(0)
                else:
                    v = None
                self._result.append(self.__create(n, v))
            else:
                n, v = k.split(sp, 2)
                self._result.append(self.__create(n, v))

        elif k.startswith('-'):
            if len(k) == 1:
                return self.__raise_unknown_name(k)
            for x in k[1:]:
                self._result.append(self.__create(x, None))

        else:
            self._result.append(self.__create(None, k))

    def resolve(self):
        while len(self._args) > 0:
            self.__resolve_argument()
        return tuple(self._result)


class Arguments:
    def __init__(self, argv):
        self._filename = argv[0]

        args = []
        index = 0
        for arg in argv[1:]:
            if arg.startswith('--'):
                raise NotImplementedError
            elif arg.startswith('-'):
                raise NotImplementedError
            else:
                index += 1
        self._args = tuple(args)


class ArgumentValue:
    TypeConverter = StringTypeConverter

    def __init__(self, index: int, name: str, value: str):
        if value and value[0] == '\\':
            value = value[1:]
        self._index = index
        self._name = name
        self._value = value

    @property
    def index(self):
        return self._index

    def __iter__(self):
        yield self._name
        yield self._value

    def value(self, annotation):
        if annotation is Parameter.empty:
            return self._value
        if isinstance(annotation, type):
            return self.TypeConverter.convert(annotation, self._value)
        raise ApiNotSupportException('annotation of parameter must be type.')

    def __repr__(self):
        fmtext = '[{index}] {name}: {value}'\
            .format(index=self._index, name=self._name, value=self._value)
        return fmtext

