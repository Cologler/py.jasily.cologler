#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from ..exceptions import ArgumentTypeException
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

    def add(self, obj):
        self._rootcmd.register(obj)
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


class Engine(IEngine):
    def __init__(self, builder: EngineBuilder):
        self._rootcmd = builder._rootcmd
        self._converter = builder.converter

    @property
    def converter(self):
        return self._converter

    def execute(self, argv, keep_error=False):
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

        s = Session(self, argv)
        try:
            return self._rootcmd.invoke(s)
        except RuntimeException as err:
            print(err.message)
        except CliException as err:
            if keep_error:
                raise
            else:
                print(err.message)
                return s.usage()
