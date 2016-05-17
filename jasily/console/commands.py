#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import inspect
from jasily.console import ArgumentsParser
from jasily.console import MissingArgumentError

class CommandDefinitionError(Exception):
    def __init__(self, msg):
        self._msg = msg
    def __str__(self):
        return self._msg

def command(alias=[], desc=''):
    '''
    may a func to a Command object. you can manual call func by func property.
    '''
    class Meta:
        def __init__(self, func):
            self._func = func
            argspec = inspect.getfullargspec(func)
            if argspec[1] is None and argspec[2] is None:
                args = argspec[0]
                if len(args) < 2:
                    raise CommandDefinitionError(\
                        'command must contains cmd & args as first & second parameter.')
                defs = argspec[3]
                if defs is None:
                    self._require_args = list(args)
                    self._optional_args = []
                else:
                    self._require_args = args[:-len(defs)]
                    self._optional_args = list(zip(args[-len(defs):], defs))
            else:
                raise CommandDefinitionError('command cannot contains varargs or varkeywords')
        @property
        def name(self):
            return self._func.__name__
        @property
        def func(self):
            return self._func
        @property
        def require_args(self):
            return self._require_args[2:]
        @property
        def optional_args(self):
            return list([x[0] for x in self._optional_args])
        def names(self):
            yield self.name
            for name in alias:
                yield name
        def execute(self, command, args):
            assert isinstance(args, ArgumentsParser)
            exe_args = []
            exe_args.append((self._require_args[0], command))
            exe_args.append((self._require_args[1], args))
            for key in self.require_args:
                try:
                    exe_args.append((key, args.get_or_error(key)))
                except MissingArgumentError as err:
                    print('error on command %s : %s' % (self.name, err))
                    return
            for arg in self._optional_args:
                exe_args.append((arg[0], args.get(arg[0], arg[1])))
            self.func(**dict(exe_args))
    return Meta

class CommandManager:
    def __init__(self):
        self._commands = []
        self._commands_mapper = {}

    def register(self, cmd):
        '''register a command.'''
        self._commands.append(cmd)
        for name in cmd.names():
            self._commands_mapper[name] = cmd
        return self

    def execute(self, argv):
        '''execute command by argv.'''
        args = ArgumentsParser(argv)
        if len(args) < 2:
            print('missing command')
            self.print_commands()
            return False
        command = self._commands_mapper.get(args[1])
        if command is None:
            print('unknown command: ' + args[1])
            self.print_commands()
            return False
        command.execute(args[1], args)
        return True

    def print_commands(self):
        print('usage:')
        for command in self._commands:
            requires = ', '.join(command.require_args)
            print('   %s\t\t%s' % (command.name, requires))
