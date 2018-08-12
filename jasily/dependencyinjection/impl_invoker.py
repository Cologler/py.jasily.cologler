#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from inspect import Parameter, isfunction, signature
from typing import List

from ..objects import NOT_FOUND
from .errors import TypeNotFoundError


class IFunctionInvoker:
    '''a interface for FunctionInvoker'''
    def invoke(self, func: callable):
        raise NotImplementedError

class IValueFactory:
    '''a interface for ValueFactory'''
    @property
    def type(self) -> type:
        '''get value type from factory.'''
        raise NotImplementedError

    def value(self) -> object:
        '''get or create value from factory.'''
        raise NotImplementedError

class SingletonValueFactory(IValueFactory):
    def __init__(self, instance: object):
        super().__init__()
        self._type = type(instance)
        self._instance = instance

    def __str__(self):
        return '%s(%s)' % (self._type.__name__, self._instance, )

    @property
    def type(self) -> type:
        return self._type

    def value(self) -> object:
        return self._instance

class CallableValueFactory(IValueFactory):
    def __init__(self, func: callable, return_value, invoker: IFunctionInvoker):
        super().__init__()

        if not callable(func):
            raise TypeError

        self._func = func
        self._signature = signature(func)

        self._type = return_value
        if self._type is None and self._signature.return_annotation != Parameter.empty:
            self._type = self._signature.return_annotation
        if not isinstance(self._type, type):
            raise TypeError

        self._invoker = invoker
        if self._invoker != None:
            if not isinstance(self._invoker, IFunctionInvoker):
                raise TypeError

    def __str__(self):
        if isinstance(self._func, type):
            return self._func.__qualname__ + '()'
        elif isfunction(self._func):
            if self._func.__name__ == '<lambda>':
                return 'lambda: -> %s' % self._type.__name__
        return self._func.__qualname__ + '()'

    @property
    def type(self) -> type:
        return self._type

    def value(self) -> object:
        if self._invoker != None:
            return self._invoker.invoke(self._func)
        else:
            return self._func()

class IFactoryRouter:
    pass

class FactoryRouter(IFactoryRouter):
    def __init__(self):
        self._count = 0
        self._current = None
        self._map = None
        self._last = None

    @property
    def count(self):
        return self._count

    def __str__(self):
        lines = []
        if self._current != None:
            lines.append(str(self._current))
        if self._map != None:
            total = len(self._map)
            for index, key in enumerate(self._map):
                header = '└' if index == total - 1 else '├'
                for subindex, subline in enumerate(str(self._map[key]).splitlines()):
                    if subindex == 0:
                        key_str = str(key)
                        if isinstance(key, type):
                            key_str = 'type(%s)' % key.__name__
                        lines.append('    %s%s: %s' % (header, key_str, subline))
                    else:
                        lines.append('     %s' % (subline))
        return '\r\n'.join(lines)

    def provide(self, factory: IValueFactory, keys: tuple, key_index: int=0):
        self._count += 1
        self._last = factory
        if len(keys) == key_index:
            self._current = factory
        else:
            key = keys[key_index]
            if self._map is None:
                self._map = {}
            resolver = self._map.get(key)
            if resolver is None:
                resolver = FactoryRouter()
                self._map[key] = resolver
            resolver.provide(factory, keys, key_index + 1)

    def resolve(self, keys: tuple, allow_last: bool=False, key_index: int=0) -> IValueFactory:
        '''return factory if found. else return None.'''
        if len(keys) == key_index:
            if self._current != None:
                return self._current
        else:
            key = keys[key_index]
            if self._map != None:
                resolver = self._map.get(key)
                if resolver != None:
                    return resolver.resolve(keys, allow_last, key_index + 1)
        if allow_last and self._last != None:
            return self._last
        return None

class Resolver:
    RESOLVE_LEVEL_ELSE = 0
    RESOLVE_LEVEL_WHOLE = 1
    RESOLVE_LEVELS = (RESOLVE_LEVEL_WHOLE, RESOLVE_LEVEL_ELSE)

    def __init__(self, **kwargs):
        self._provided = []
        self._name_resolver = FactoryRouter()
        self._type_resolver = FactoryRouter()
        self._base_resolver = kwargs.get('base_resolver', None)
        assert isinstance(self._base_resolver, (Resolver, type(None)))

    def __str__(self):
        lines = []
        if self._name_resolver.count > 0:
            lines.append('[Name Resolver]')
            lines.append(str(self._name_resolver))
        if self._type_resolver.count > 0:
            lines.append('[Type Resolver]')
            lines.append(str(self._type_resolver))
        return '\r\n'.join(lines)

    def import_from(self, resolver):
        for provided in resolver._provided:
            self.provide(*provided)

    def provide(self, factory: IValueFactory,
                provide_type: type=None, provide_name: str=None) -> List[IFactoryRouter]:
        if not isinstance(provide_type, (type(None), type)):
            raise TypeError
        self._provided.append((factory, provide_type, provide_name))
        fix_type = provide_type or factory.type
        self._type_resolver.provide(factory, (fix_type, ))
        if provide_name:
            if provide_type is None:
                self._name_resolver.provide(factory, (provide_name, ))
            self._name_resolver.provide(factory, (provide_name, fix_type))

    def resolve(self, parameter_name: str, expected_type: type=None) -> object:
        '''
        resolve value for request parameter.
        return NOT_FOUND if not resolved.
        '''
        factory = self.resolve_factory(parameter_name, expected_type)
        if factory != None:
            return factory.value()
        else:
            return NOT_FOUND

    def resolve_factory(self, parameter_name: str, expected_type: type=None) -> IValueFactory:
        '''
        resolve factory for request parameter.
        return None if not resolved.
        '''
        for level in Resolver.RESOLVE_LEVELS:
            factory = self._resolve_core(parameter_name, expected_type, level)
            if factory is None and self._base_resolver != None:
                factory = self._base_resolver._resolve_core(parameter_name, expected_type, level)
            if factory:
                return factory
        return None

    def _resolve_core(self, parameter_name: str, expected_type: type, level: int) -> IValueFactory:
        if level == Resolver.RESOLVE_LEVEL_WHOLE:
            return self._resolve_core_whole(parameter_name, expected_type)
        elif level == Resolver.RESOLVE_LEVEL_ELSE:
            return self._resolve_core_else(parameter_name, expected_type)
        else:
            raise NotImplementedError

    def _enumerate_type(self, expected_type: type):
        if isinstance(expected_type, type):
            yield expected_type
        elif isinstance(expected_type, tuple):
            for etype in expected_type:
                yield etype

    def _resolve_core_whole(self, parameter_name: str, expected_type: type) -> IValueFactory:
        if expected_type is None:
            return self._name_resolver.resolve((parameter_name, ), False)
        else:
            for etype in self._enumerate_type(expected_type):
                factory = self._name_resolver.resolve((parameter_name, etype), False)
                if factory != None:
                    return factory
        return None

    def _resolve_core_else(self, parameter_name: str, expected_type: type) -> IValueFactory:
        if expected_type != None:
            for etype in self._enumerate_type(expected_type):
                factory = self._type_resolver.resolve((etype, ), False)
                if factory != None:
                    return factory
        return None

class ArgumentFiller:
    '''fill the actual argument.'''
    def __init__(self, parameter: Parameter):
        self._parameter = parameter
        self._is_filled = False
        self._value = None

    @property
    def name(self):
        '''get name of parameter.'''
        return self._parameter.name

    @property
    def is_require(self) -> bool:
        '''whether the argument must be fill.'''
        return self._parameter.default == Parameter.empty

    @property
    def is_filled(self) -> bool:
        '''whether the argument is filled.'''
        return self._is_filled

    @property
    def value(self) -> object:
        '''get value after filled.'''
        if self._is_filled:
            return self._value
        if self.is_require:
            raise TypeNotFoundError
        return self._parameter.default

    def fill(self, resolver: Resolver) -> None:
        '''fill the argument.'''
        expected_type = self._parameter.annotation\
            if self._parameter.annotation != Parameter.empty\
            else None
        value = resolver.resolve(self._parameter.name, expected_type)
        if value != NOT_FOUND:
            self._value = value
            self._is_filled = True

class FunctionInvoker(IFunctionInvoker):
    def __init__(self, **kwargs):
        super().__init__()
        self._resolver = Resolver(**kwargs)

    def __str__(self):
        return str(self._resolver)

    def invoke(self, func: callable):
        '''invoke to execute the func.'''
        sign = signature(func)
        if len(sign.parameters) > 0:
            fillers = [ArgumentFiller(x) for x in sign.parameters.values()]
            for filler in fillers:
                filler.fill(self._resolver)
            kwargs = dict(zip([x.name for x in fillers], [x.value for x in fillers]))
            return func(**kwargs)
        else:
            return func()

    def provide_object(self, obj: object,
                       provide_type: type=None, provide_name: str=None):
        '''provide singleton argument.'''
        if provide_type != None and not isinstance(obj, provide_type):
            raise TypeError
        factory = SingletonValueFactory(obj)
        self._resolver.provide(factory, provide_type, provide_name)

    def provide_callable(self, func: callable,
                         provide_type: type=None, provide_name: str=None,
                         invoker=None):
        '''provide factory func to create argument.'''
        factory = CallableValueFactory(func, provide_type, invoker)
        self._resolver.provide(factory, provide_type, provide_name)

    def provide_type(self, provide_type: type, provide_name: str=None,
                     invoker=None):
        '''provide type to create argument.'''
        func = provide_type
        if provide_type is list:
            func = lambda: []
        elif provide_type is dict:
            func = lambda: {}
        self.provide_callable(func, provide_type, provide_name, invoker)

    def create_transient(self):
        '''create a overrideable invoker from this.'''
        invoker = FunctionInvoker(base_resolver=self._resolver)
        return invoker
