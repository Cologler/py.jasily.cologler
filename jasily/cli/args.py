#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------


from enum import Enum
from inspect import Parameter
from ..exceptions import ApiNotSupportException, ArgumentValueException


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

def __init_ENGLISG():
    e1 = ''.join([chr(x) for x in range(ord('a'), ord('z') + 1)])
    e2 = ''.join([chr(x) for x in range(ord('A'), ord('Z') + 1)])
    return e1 + e2
ENGLISG = __init_ENGLISG()

class ArgumentParser:
    NAME_FIRST_CHARS = ENGLISG + '_-'
    NAME_CHARS = NAME_FIRST_CHARS + '0123456789'

    def __init__(self, args: list):
        self._raw_args = args
        self._args = args.copy()
        self._result = []
        self._spliters = ('=', ':')

    def __raise_argument_name(self, value: str, tryvalue: str):
        msg = '{value} is invalid argument name. '
        msg += "if you want to use '{tryvalue}', try input '\\{tryvalue}'"
        raise ArgumentValueException(value, msg, tryvalue=tryvalue)

    def __check_argument_name(self, name: str):
        if len(name) == 0:
            raise NotImplementedError
        def raise_err():
            self.__raise_argument_name(name, name)
        if name[0] not in self.NAME_FIRST_CHARS:
            raise_err()
        for c in name[1:]:
            if c not in self.NAME_CHARS:
                raise_err()

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
            try:
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
            except ArgumentValueException as err:
                self.__raise_argument_name(n, '--' + n)
                raise

        elif k.startswith('-'):
            if len(k) == 1:
                return self.__raise_unknown_name(k)
            for x in k[1:]:
                try:
                    self._result.append(self.__create(x, None))
                except ArgumentValueException as err:
                    self.__raise_argument_name(x, '-' + x)
                    raise

        else:
            self._result.append(self.__create(None, k))

    def resolve(self):
        while len(self._args) > 0:
            self.__resolve_argument()
        return tuple(self._result)

class ArgumentKinds(Enum):
    '''argument kinds.'''
    NameValuePair = 0
    NameOnly = 1
    ValueOnly = 2


class ArgumentValue:
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

    @property
    def name(self):
        return self._name

    @property
    def has_value(self):
        return self._value != None

    @property
    def kind(self) -> ArgumentKinds:
        '''get argument kind.'''
        if self._name is None:
            return ArgumentKinds.ValueOnly
        elif self._value is None:
            return ArgumentKinds.NameOnly
        else:
            return ArgumentKinds.NameValuePair

    def value(self, converter, annotation):
        if annotation is Parameter.empty:
            return self._value
        if isinstance(annotation, type):
            return converter.convert(annotation, self._value)
        raise ApiNotSupportException('annotation of parameter must be type.')

    def __str__(self):
        if self._value is None:
            return '--' + self._name
        elif self._name is None:
            return self._value
        else:
            fmtext = '({name}: {value})'\
                .format(index=self._index, name=self._name, value=self._value)
            return fmtext

    def __repr__(self):
        fmtext = '[{index}] {name}: {value}'\
            .format(index=self._index, name=self._name, value=self._value)
        return fmtext


class Arguments:
    def __init__(self, argv):
        self._filename = argv[0]
        self._raw_args = tuple(argv[1:])
        self._var_args = list(argv[1:])

    @property
    def filename(self):
        return self._filename

    def try_popcmd(self):
        if len(self._var_args) > 0:
            return self._var_args.pop(0)
        else:
            return None

    def to_args(self):
        return ArgumentParser(self._var_args).resolve()
