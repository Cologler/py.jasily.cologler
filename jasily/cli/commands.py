#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from inspect import signature, Parameter

from ..utils.objects import Freezable
from ..exceptions import (
    InvalidOperationException,
    ArgumentValueException,
    InvalidArgumentException
)
from ..convert import TypeConvertException

from .exceptions import NameConflictException, ParameterException
from .typed import *
from .descriptors import *
from .args import Arguments, ArgumentValue


class Session(ISession, Freezable):
    def __init__(self, engine, argv, state):
        self._engine = engine
        self._args = Arguments(argv)
        self._state = state
        self._instance = None
        self._cmdchain = []

    @property
    def state(self):
        return self._state

    @property
    def args(self):
        return self._args

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, value):
        self.raise_if_freezed()
        self._instance = value

    @property
    def engine(self):
        return self._engine

    def add_cmd(self, cmd):
        self.raise_if_freezed()
        self._cmdchain.append(cmd)

    def cmds(self):
        return tuple(self._cmdchain)

    def usage(self):
        strings = CommandUsageFormater(self).strings()
        print('\n'.join(strings))


class BaseCommand(Freezable):
    def __init__(self):
        self._subcmds = []
        self._subcmds_map = {}
        self._has_name = None

    def freeze(self):
        if len(self._subcmds) == 1:
            self._subcmds[0]._has_name = False
        super().freeze()
        for c in self._subcmds:
            c.freeze()

    def register(self, obj, name=None, **kwargs):
        self.raise_if_freezed()

        # build command
        descriptor = describe(obj, name)
        if isinstance(descriptor, CallableDescriptor):
            cmd = CallableCommand(descriptor)
        elif isinstance(descriptor, PropertyDescriptor):
            cmd = PropertyCommand(descriptor)
        elif isinstance(descriptor, (TypeDescriptor, InstanceDescriptor)):
            cmd = ClassCommand(descriptor)
        else:
            raise NotImplementedError

        # from kwargs
        if len(kwargs) > 0:
            alias = kwargs.pop('alias', '')
            if alias:
                cmd.add_alias(alias)
        if len(kwargs) > 0:
            raise InvalidArgumentException(kwargs.keys()[0])

        # map command
        for name in cmd.enumerate_names():
            cc = self._subcmds_map.get(name)
            if cc != None and cc != cmd:
                raise NameConflictException(name, "'{name}' is already exists.")
            self._subcmds_map[name] = cmd
        self._subcmds.append(cmd)

    def invoke(self, s: Session):
        args = s.args
        if len(self._subcmds) == 0:
            raise NotImplementedError
        elif len(self._subcmds) == 1:
            return self._subcmds[0].invoke(s)
        else:
            cmd = args.try_popcmd()
            sc = None
            if cmd != None:
                sc = self._subcmds_map.get(cmd.lower())
            if sc is None:
                return s.usage()
            return sc.invoke(s)

    @property
    def has_name(self):
        return False

    @property
    def can_execute(self):
        return False

    def subcmds(self):
        return tuple(self._subcmds)


class Command(BaseCommand):
    def __init__(self, descriptor: Descriptor):
        super().__init__()
        self._doc = None
        self._descriptor = descriptor
        self._names = []
        for name in self._descriptor.enumerate_names():
            if name:
                self._names.append(name.lower().replace('_', '-'))

    @property
    def doc(self):
        '''get doc from command.'''
        return self._doc or self._descriptor.doc

    @property
    def descriptor(self):
        return self._descriptor

    def enumerate_names(self):
        for n in self._names:
            yield n

    @property
    def has_name(self):
        if self._has_name is None:
            return len(self._subcmds) != 1 and self._descriptor != None
        return self._has_name

    def invoke(self, s: Session):
        s.add_cmd(self)
        return super().invoke(s)

    def add_alias(self, name):
        if isinstance(name, str):
            self._names.append(name)
        elif isinstance(name, list):
            for n in name:
                self.add_alias(n)
        else:
            raise NotImplementedError


class ClassCommand(Command):
    def __init__(self, descriptor: Descriptor):
        super().__init__(descriptor)
        methods = [x for x in dir(self._descriptor.type) if not x.startswith('_')]
        for method in methods:
            self.register(getattr(self._descriptor.described_object, method), method)

    def invoke(self, s: Session):
        s.instance = self._descriptor.instance()
        return super().invoke(s)


class RootCommand(BaseCommand):
    pass


class ExecuteableCommand(Command):
    @property
    def can_execute(self):
        return True

    @property
    def has_parameters(self):
        return False

    def parameters(self):
        return []


class PropertyCommand(ExecuteableCommand):
    def invoke(self, s: Session):
        s.add_cmd(self)
        s.freeze()
        return getattr(s.instance, self._descriptor.name)


class CallableCommand(ExecuteableCommand):
    def __init__(self, descriptor: Descriptor):
        super().__init__(descriptor)
        self._parameters = None

    @property
    def has_parameters(self):
        if self._parameters is None:
            raise NotImplementedError
        return len(self._parameters) > 0

    def parameters(self):
        if self._parameters is None:
            raise NotImplementedError
        return list(self._parameters)

    def invoke(self, s: Session):
        s.add_cmd(self)
        i = s.instance
        # build func
        if i is None:
            func = self._descriptor.described_object
        else:
            func = getattr(i, self._descriptor.name)
        # build parameters
        if self._parameters is None:
            self._parameters = tuple(signature(func).parameters.values())
        # resolve parameters
        try:
            args, kwargs = self.resolve_parameter(s)
        except ParameterException:
            raise

        # invoke
        s.freeze()
        return func(*args, **kwargs)

    def resolve_parameter(self, s: Session):
        rargs = []
        resolvers = tuple([create_resolver(s, i, p) for i, p in enumerate(self._parameters)])

        # resolve known type
        resolving = [x for x in resolvers if type(x) is KeywordParameterResolver and x.accept_value()]
        mt = maptype(s)
        for r in resolving:
            r.resolve_by_type(mt)
        # resolve KeywordParameterResolver by name
        try:
            rargs = s.args.to_args()
        except ArgumentValueException as err:
            raise ParameterException(str(err))
        sargs = list(rargs)
        resolving = [x for x in resolving if x.accept_value()]
        for r in resolving:
            sargs = [x for x in sargs if not r.resolve_by_name(x)]
        # resolve KeywordParameterResolver by value
        resolving = [x for x in resolving if x.accept_value()]
        for r in resolving:
            sargs = [x for x in sargs if not r.resolve_by_value(x)]
        # resolve VarKeywordParameterResolver
        resolving = [x for x in resolvers if type(x) is VarKeywordParameterResolver]
        for r in resolving:
            sargs = [x for x in sargs if not r.resolve_by_name(x)]
        # resolve VarPosotionalParameterResolver
        resolving = [x for x in resolvers if type(x) is VarPosotionalParameterResolver]
        for r in resolving:
            sargs = [x for x in sargs if not r.resolve_by_value(x)]

        # check all
        if len(sargs) > 0:
            argsstr = ', '.join([str(x) for x in sargs])
            raise ParameterException('unknown arguments: <%s>' % argsstr)
        for r in resolvers:
            if not r.is_resolved():
                raise ParameterException('parameter {name} is NOT resolved.', name=r.parameter.name)
        # end
        args = []
        kwargs = {}
        for r in resolvers:
            r.build(args, kwargs)
        return args, kwargs


def create_resolver(s: Session, i: int, parameter: Parameter):
    kwargs = {
        'session': s,
        'index': i,
        'parameter': parameter
    }
    if parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
        return KeywordParameterResolver(**kwargs)
    elif parameter.kind == Parameter.VAR_POSITIONAL:
        return VarPosotionalParameterResolver(**kwargs)
    elif parameter.kind == Parameter.VAR_KEYWORD:
        return VarKeywordParameterResolver(**kwargs)
    else:
        raise NotImplementedError


class ParameterResolver:
    def __init__(self, session: Session, index: int, parameter: Parameter):
        self._session = session
        self._index = index
        self._parameter = parameter
        self._value = Parameter.empty

    @property
    def parameter(self):
        return self._parameter

    def accept_value(self):
        raise NotImplementedError

    def is_resolved(self):
        raise NotImplementedError

    def resolve_by_type(self, m: dict):
        return False

    def resolve_by_name(self, arg: ArgumentValue):
        return False

    def resolve_by_value(self, arg: ArgumentValue):
        return False

    def build(self, args: list, kwargs: dict):
        raise NotImplementedError


class KeywordParameterResolver(ParameterResolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_list = self._parameter.annotation in LIST_ARGS
        self._targrt_type = str
        if self._parameter.annotation != Parameter.empty:
            if not isinstance(self._parameter.annotation, type):
                n = str(self._parameter.annotation)
                raise InvalidOperationException('not support parameter annotation <%s>' % n)
            self._targrt_type = self._parameter.annotation
        elif self._parameter.default != Parameter.empty:
            if self._parameter.default != None:
                self._targrt_type = type(self._parameter.default)

    def accept_value(self):
        if self._is_list:
            return True
        else:
            return self._value is Parameter.empty

    def is_resolved(self):
        return self._value != Parameter.empty or self._parameter.default != Parameter.empty

    def resolve_by_type(self, m: dict):
        if self._parameter.annotation is Parameter.empty:
            return False
        self._value = m.get(self._parameter.annotation, Parameter.empty)
        return self.is_resolved()

    def __resolve_by_value(self, arg: ArgumentValue):
        t = str if self._is_list else self._targrt_type
        try:
            value = arg.value(self._session.engine.converter, t)
        except TypeConvertException as err:
            msg = 'cannot convert <"{value}"> to type <{type}>.'
            raw = arg.value(self._session.engine.converter, str)
            raise ParameterException(msg, value=raw, type=self._parameter.annotation.__name__)
        if self._is_list:
            if self._value is Parameter.empty:
                self._value = []
            self._value.append(value)
        else:
            self._value = value
        return True

    def resolve_by_name(self, arg: ArgumentValue):
        if arg.name != self._parameter.name:
            return False
        if not self._is_list and self._value != Parameter.empty:
            raise ParameterException('conflict arguments: <{name}>', name=arg.name)
        return self.__resolve_by_value(arg)

    def resolve_by_value(self, arg: ArgumentValue):
        if arg.name != None:
            return False
        if not self._is_list and self.is_resolved():
            return False
        return self.__resolve_by_value(arg)

    def build(self, args: list, kwargs: dict):
        if self._value is Parameter.empty:
            value = self._parameter.default
        elif self._is_list:
            value = self._parameter.annotation(self._value)
        else:
            value = self._value
        kwargs[self._parameter.name] = value


class _VarParameterResolver(ParameterResolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def accept_value(self):
        return True

    def is_resolved(self):
        return True


class VarPosotionalParameterResolver(_VarParameterResolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._args = []

    def resolve_by_value(self, arg: ArgumentValue):
        if arg.name != None and arg.name != self.parameter.name:
            return False
        self._args.append(arg.value(self._session.engine.converter, str))
        return True

    def build(self, args: list, kwargs: dict):
        for a in self._args:
            args.append(a)


class VarKeywordParameterResolver(_VarParameterResolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._args = {}

    def resolve_by_name(self, arg: ArgumentValue):
        if arg.name != None or arg.name != self.parameter.name:
            return False
        if arg.name in self._args:
            raise ParameterException('conflict arguments: <{name}>', name=arg.name)
        self._args[arg.name] = arg.value(self._session.engine.converter, str)
        return True

    def build(self, args: list, kwargs: dict):
        for k in self._args:
            kwargs[k] = args


class CommandUsageFormater:
    def __init__(self, s: Session):
        self._session = s
        self._docs = []

    def _parse_parameter(self, p: Parameter):
        if p.default is Parameter.empty:
            name = p.name.upper()
        else:
            name = '--' + p.name

        if p.annotation != Parameter.empty:
            if p.annotation is str:
                pass
            elif p.annotation in LIST_ARGS:
                name = '[%s,...]' % name
            else:
                name += ':' + p.annotation.__name__

        if p.default != Parameter.empty:
            name += ' ?'

        return name

    def strings(self) -> list:
        docs = self._docs
        docs.append('Usage:')

        parts = []
        parts.append(self.on_filename())

        trees = list(self._session.cmds())
        names = list([list(x.enumerate_names())[0] for x in trees if x.has_name])
        for n in names:
            parts.append(n)
        header = '   ' + ' '.join(parts)

        for l in self.on_cmd(trees[-1] if len(trees) > 0 else self._session.engine.rootcmd):
            docs.append(header + ' ' + l)
        return docs

    def on_filename(self) -> str:
        fn = self._session.args.filename
        if ' ' in fn:
            return '"' + fn + '"'
        else:
            return fn

    def on_cmd(self, cmd: Command):
        if cmd.can_execute:
            return self.on_execcmd(cmd)
        else:
            return self.on_treecmd(cmd)

    def on_treecmd(self, cmd: Command):
        sc = cmd.subcmds()
        if len(sc) == 1:
            return self.on_cmd(cmd)
        for c in sc:
            ns = list(c.enumerate_names())
            assert len(ns) > 0
            if len(ns) == 1:
                yield ns[0]
            else:
                yield '%s (%s)' % (ns[0], '/'.join(ns[1:]))

    def on_execcmd(self, cmd: ExecuteableCommand):
        if cmd.has_parameters:
            parts = []
            for p in cmd.parameters():
                parts.append(self._parse_parameter(p))
            yield ' '.join(parts)
        else:
            yield ''
        doc = cmd.doc
        if doc:
            for line in doc.splitlines():
                self._docs.append(' ' * 6 + line)
