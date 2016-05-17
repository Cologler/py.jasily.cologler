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

def command(alias=[], desc=None):
    '''
    may a func to a Command object. you can manual call func by func property.
    '''
    class Meta:
        def __init__(self, func):
            self._desc = desc or func.__doc__ or '%s command.' % func.__name__
            self._func = func
            self._alias = alias
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

        def names(self):
            yield self.name
            for name in self.alias:
                yield name

        @property
        def alias(self):
            return self._alias

        @property
        def desc(self):
            return self._desc
        
        @property
        def func(self):
            return self._func
        
        @property
        def require_args(self):
            return self._require_args[2:]
        
        @property
        def optional_args(self):
            return list(self._optional_args)
        
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

class _CommandWrapper:
    def __init__(self, cmd):
        self.command = cmd
        self.is_enable = True

class CommandManager:
    def __init__(self):
        self._commands = []
        self._commands_mapper = {}
        self._max_command_length = 0

    def register(self, cmd):
        '''register a command.'''
        wrapper = _CommandWrapper(cmd)
        self._commands.append(wrapper)
        for name in cmd.names():
            name_fixed = name.replace('_', '-')
            self._max_command_length = max(self._max_command_length, len(name_fixed))
            self._commands_mapper[name_fixed] = wrapper
        return self

    def execute(self, argv):
        '''execute command by argv.'''
        args = ArgumentsParser(argv)
        if len(args) < 2:
            print('missing command')
            self.print_commands()
            return False
        wrapper = self._commands_mapper.get(args[1])
        if wrapper is None:
            print('unknown command: ' + args[1])
            self.print_commands()
            return False
        wrapper.command.execute(args[1], args)
        return True

    def print_commands(self):
        print('usage:')
        for command in [x.command for x in self._commands if x.is_enable]:
            name = ('   ' + command.name).ljust(self._max_command_length) + '\t' + command.desc
            print(name)
            padding = ''.ljust(self._max_command_length) + '\t'
            buffer_max = 80
            if len(command.require_args) > 0:
                buffer = 'require: '
                for arg in ['-%s' % z for z in command.require_args]:
                    if len(arg) + len(buffer) > buffer_max:
                        print(padding + buffer)
                        buffer = ''
                    buffer += (' ' + arg if len(buffer) > 0 else arg)
                if len(buffer) > 0:
                    print(padding + buffer)
                    buffer = ''
            if len(command.optional_args) > 0:
                buffer = 'optional: '
                for arg in ['[-%s=%s]' % (z[0], z[1]) for z in command.optional_args]:
                    if len(arg) + len(buffer) > buffer_max:
                        print(padding + buffer)
                        buffer = ''
                    buffer += (' ' + arg if len(buffer) > 0 else arg)
                if len(buffer) > 0:
                    print(padding + buffer)
                    buffer = ''
            if len(command.alias) > 0:
                print(' ' * 6 + 'alias: ' + ', '.join(command.alias))

