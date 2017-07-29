#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from ..d import descriptor
from ..exceptions import ArgumentTypeException, InvalidOperationException
from ..convert import StringTypeConverter
from .exceptions import (
    CliException,
    RuntimeException
)
from .typed import (
    IEngine,
    IFile, IFolder
)
from .commands import (
    Session,
    Command, RootCommand
)


class CliStringTypeConverter(StringTypeConverter):
    def to_file(self, v) -> IFile:
        if os.path.isfile(v):
            return IFile(v)
        raise ValueError

    def to_folder(self, v) -> IFolder:
        if os.path.isfile(v):
            return IFolder(v)
        raise ValueError


class EngineBuilder:
    def __init__(self):
        self._rootcmd = RootCommand()
        self._converter = CliStringTypeConverter()

    def add(self, obj, **kwargs):
        self._rootcmd.register(obj, **kwargs)
        return self

    def build(self):
        self._rootcmd.freeze()
        return Engine(self)

    @property
    def converter(self):
        return self._converter

    @converter.setter
    def converter(self, value):
        if not isinstance(value, CliStringTypeConverter):
            raise ArgumentTypeException(CliStringTypeConverter, value)
        self._converter = value

    @descriptor
    def command(self, *args, **kwargs):
        '''
        command(func) -> func
        command(alias) -> descriptor
        '''
        if len(args) > 0:
            if len(kwargs) > 0:
                raise InvalidOperationException
            if len(args) != 1:
                raise InvalidOperationException
        if len(args) == 1 and len(kwargs) == 0:
            self.add(args[0])
            return args[0]
        def wrap(func):
            return self.add(func, **kwargs)
        return wrap


class Engine(IEngine):
    def __init__(self, builder: EngineBuilder):
        self._rootcmd = builder._rootcmd
        self._converter = builder.converter

    @property
    def rootcmd(self):
        return self._rootcmd

    @property
    def converter(self):
        return self._converter

    def execute(self, argv, keep_error=False, state=None):
        if argv is None:
            raise ValueError
        if isinstance(argv, tuple):
            argv = list(argv)
        elif isinstance(argv, str):
            argv = [argv]
        elif not isinstance(argv, list):
            raise ValueError

        if len(argv) == 0:
            argv.append(sys.argv[0])
        elif argv[0] != sys.argv[0]:
            argv.insert(0, sys.argv[0])

        def print_error(msg):
            colorama = None
            try:
                import colorama
            except ModuleNotFoundError:
                pass
            if colorama != None:
                colorama.init()
                msg = colorama.Fore.LIGHTRED_EX + msg
                msg += colorama.Style.RESET_ALL
            print(msg)

        s = Session(self, argv, state)
        try:
            return self._rootcmd.invoke(s)
        except RuntimeException as err:
            print_error(err.message)
        except CliException as err:
            if keep_error:
                raise
            else:
                print_error(err.message)
                return s.usage()
