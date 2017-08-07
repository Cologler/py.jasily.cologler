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

from .exceptions import ApplicationException, UserInputException
from .typed import *
from .descriptors import *
from .args import Arguments, ArgumentValue, ArgumentKinds

try:
    import colorama
    colorama.init()
    Fore_LIGHTYELLOW = colorama.Fore.LIGHTYELLOW_EX
    Style_RESET_ALL = colorama.Style.RESET_ALL
except ModuleNotFoundError:
    Fore_LIGHTYELLOW = ''
    Style_RESET_ALL = ''


class Session(ISession, Freezable):
    def __init__(self, engine, argv, state):
        self._engine = engine
        self._args = Arguments(argv)
        self._state = state
        self._instance = None
        self._cmdchain = []
        self._auto_resolve_map = {
            IEngine: engine,
            ISession: self
        }

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
        '''router commands.'''
        return tuple(self._cmdchain)

    def usage(self):
        strings = CommandUsageFormater(self).strings()
        print('\n'.join(strings))

    @property
    def auto_resolve_map(self):
        return self._auto_resolve_map



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
                msg = "'{name}' is already exists.".format(name=name)
                raise ApplicationException(msg)
            self._subcmds_map[name] = cmd
        self._subcmds.append(cmd)

    def invoke(self, s: Session):
        args = s.args
        if len(self._subcmds) == 0:
            raise NotImplementedError('There are no implemented commands.')
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
        self._doc = None # command doc from engine builder.
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
        except UserInputException:
            raise

        # invoke
        s.freeze()
        return func(*args, **kwargs)

    def resolve_parameter(self, s: Session):
        rargs = []
        resolvers = tuple([create_resolver(s, i, p) for i, p in enumerate(self._parameters)])

        # resolve known type
        resolving = [x for x in resolvers if type(x) is KeywordParameterResolver and x.can_accept()]
        for r in resolving:
            r.resolve_from(s)
        # resolve KeywordParameterResolver by name
        try:
            rargs = s.args.to_args()
        except ArgumentValueException as err:
            raise UserInputException(str(err))
        sargs = list(rargs)
        resolving = [x for x in resolving if x.can_accept()]
        for r in resolving:
            sargs = [x for x in sargs if not r.resolve_by_name(x)]
        # resolve KeywordParameterResolver by value
        resolving = [x for x in resolving if x.can_accept()]
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
            raise UserInputException('unknown arguments: <%s>' % argsstr)
        for r in resolvers:
            if not r.is_resolved():
                raise UserInputException('parameter {name} is NOT resolved.'.format(name=r.parameter.name))
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

    def can_accept(self):
        raise NotImplementedError

    def is_resolved(self):
        raise NotImplementedError

    def resolve_from(self, source: Session):
        '''resolve parameter value from session.'''
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

    def can_accept(self):
        return self._is_list or self._value is Parameter.empty

    def is_resolved(self):
        return self._value != Parameter.empty or self._parameter.default != Parameter.empty

    def resolve_from(self, source: Session):
        if self._parameter.annotation is Parameter.empty:
            return False
        self._value = source.auto_resolve_map.get(self._parameter.annotation, Parameter.empty)
        return self.is_resolved()

    def __resolve_by_value(self, arg: ArgumentValue):
        t = str if self._is_list else self._targrt_type
        try:
            value = arg.value(self._session.engine.converter, t)
        except TypeConvertException as err:
            msg = 'cannot convert <"{value}"> to type <{type}>.'
            raw = arg.value(self._session.engine.converter, str)
            msg = msg.format(value=raw, type=self._parameter.annotation.__name__)
            raise UserInputException(msg)
        self.__set_value(value)
        return True

    def __set_value(self, value):
        if self._parameter.annotation != None:
            assert isinstance(value, self._parameter.annotation)
        if self._is_list:
            if self._value is Parameter.empty:
                self._value = []
            self._value.append(value)
        elif self._value is Parameter.empty:
            self._value = value
        else:
            raise NotImplementedError

    def resolve_by_name(self, arg: ArgumentValue):
        if arg.name != self.parameter.name:
            return False
        if not self._is_list and self._value != Parameter.empty:
            # already has value
            raise UserInputException('Conflict arguments: <{}>'.format(arg.name))
        if arg.kind == ArgumentKinds.NameOnly:
            if self.parameter.annotation != bool:
                msg = ['Unkown arguments: <{}>'.format(arg.name)]
                msg.append('   Hint: you may try to use `--{0}` instead `-{0}`'.format(arg.name))
                raise UserInputException('\n'.join(msg))
            else:
                self.__set_value(True)
        else:
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

    def can_accept(self):
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
            raise UserInputException('conflict arguments: <{name}>'.format(name=arg.name))
        self._args[arg.name] = arg.value(self._session.engine.converter, str)
        return True

    def build(self, args: list, kwargs: dict):
        for k in self._args:
            kwargs[k] = args


class UsageOptions:
    def __init__(self):
        self._show_doc = True

    @property
    def show_doc(self):
        '''get whether show doc on list commands.'''
        return self._show_doc

    @show_doc.setter
    def show_doc(self, value):
        '''set whether show doc on list commands.'''
        self._show_doc = value


class CommandUsageFormater:
    def __init__(self, s: Session):
        self._session = s
        self._options = s.engine.options.usage_options
        self._docs = []
        self._indent_unit = 3

    def _parse_parameter(self, p: Parameter):
        if p.annotation in self._session.auto_resolve_map:
            return

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

    def indent(self, index: int):
        return ' ' * self._indent_unit * index

    def strings(self) -> list:
        docs = self._docs
        docs.append(Fore_LIGHTYELLOW + 'Usage:' + Style_RESET_ALL)
        docs.append(self.indent(1) + Fore_LIGHTYELLOW + 'Script Path:' + Style_RESET_ALL)
        docs.append(self.indent(2) + self.get_filename())

        parts = []
        trees = list(self._session.cmds())
        if len(trees) > 0:
            names = list([list(x.enumerate_names())[0] for x in trees if x.has_name])
            for n in names:
                parts.append(n)
            header = ' '.join(parts)
            docs.append(self.indent(1) + Fore_LIGHTYELLOW + 'Route Commands: ' + Style_RESET_ALL)
            docs.append(self.indent(2) + header)

        self.on_cmd(trees[-1] if len(trees) > 0 else self._session.engine.rootcmd)
        return docs

    def get_filename(self) -> str:
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
        docs = self._docs
        docs.append(self.indent(1) + Fore_LIGHTYELLOW + 'Accept sub Commands:' + Style_RESET_ALL)
        for c in sc:
            ns = list(c.enumerate_names())
            assert len(ns) > 0
            if len(ns) == 1:
                line = ns[0]
            else:
                line = '%s (%s)' % (ns[0], '/'.join(ns[1:]))
            docs.append(self.indent(2) + line)
            if self._options.show_doc:
                if c.doc != None:
                    docs.append(self.indent(3) + c.doc)

    def on_execcmd(self, cmd: ExecuteableCommand):
        docs = self._docs
        if cmd.has_parameters:
            docs.append(self.indent(1) + Fore_LIGHTYELLOW + 'Parameters:' + Style_RESET_ALL)
            parts = []
            for p in cmd.parameters():
                parts.append(self._parse_parameter(p))
            docs.append(self.indent(2) + ' '.join([x for x in parts if x]))
        else:
            pass
        doc = cmd.doc
        if doc:
            docs.append(self.indent(1) + Fore_LIGHTYELLOW + 'Description:' + Style_RESET_ALL)
            for line in doc.splitlines():
                docs.append(self.indent(2) + line)
