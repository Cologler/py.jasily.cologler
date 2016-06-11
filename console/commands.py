#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import inspect
from jasily.console import ConsoleArguments
from jasily.console import MissingArgumentError

class CommandDefinitionError(Exception):
    '''user program error.'''
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg

class CommandRunningError(Exception):
    '''command end without finish. this Exception can safe call in command.'''
    def __init__(self, msg):
        super().__init__()
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
                if len(args) < 1:
                    raise CommandDefinitionError(\
                        'command must contains session as first parameter.')
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
            '''get command name.'''
            return self._func.__name__.replace('_', '-')

        def names(self):
            '''yield command name and alias.'''
            yield self.name
            for name in self.alias:
                yield name

        @property
        def alias(self):
            '''get command alias.'''
            return self._alias

        @property
        def desc(self):
            '''get command desc.'''
            return self._desc

        @property
        def func(self):
            return self._func

        @property
        def require_args(self):
            '''get require args.'''
            return self._require_args[1:]

        @property
        def optional_args(self):
            '''get optional args.'''
            return list(self._optional_args)

        def execute(self, session):
            '''execute command. possible raise CommandRunningError.'''
            assert isinstance(session, CommandSession)
            exe_args = []
            exe_args.append((self._require_args[0], session))
            for key in self.require_args:
                arg_name = key
                try:
                    exe_args.append((arg_name, session.args.get_or_error(key)))
                except MissingArgumentError as err:
                    print('error on command %s : %s' % (self.name, err))
                    return
            for arg in self._optional_args:
                arg_name = arg[0]
                arg_defval = arg[1]
                arg_val = session.args.get(arg_name, arg_defval)
                if arg_val != arg_defval and type(arg_val) != type(arg_defval):
                    assert isinstance(arg_val, str)
                    if isinstance(arg_defval, int):
                        if not arg_val.isdigit():
                            raise CommandRunningError('arg %s should be digit.' % arg_name)
                        arg_val = int(arg_val)
                exe_args.append((arg[0], arg_val))
            self.func(**dict(exe_args))
    return Meta

class _CommandWrapper:
    def __init__(self, cmd):
        self.command = cmd
        self.is_enable = True

class CommandSession:
    '''parameter of @command'''
    def __init__(self, manager, args):
        assert isinstance(manager, CommandManager)
        assert isinstance(args, ConsoleArguments)
        self._manager = manager
        self._args = args

    @property
    def command_manager(self):
        '''get caller CommandManager object.'''
        return self._manager

    @property
    def args(self):
        '''get args parser for this session.'''
        return self._args

    @property
    def command(self):
        '''get command text which route to current command.'''
        return self._args[1]

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

    def command(self, alias=[], desc=None):
        '''create and register command.'''
        cmd = command(alias, desc)
        def wrap(func):
            self.register(command(alias, desc)(func))
        return wrap

    def execute(self, argv):
        '''execute command by argv.'''
        args = ConsoleArguments(argv)
        if len(args) < 2:
            print('missing command')
            self.print_commands()
            return False
        wrapper = self._commands_mapper.get(args[1])
        if wrapper is None:
            print('unknown command: ' + args[1])
            self.print_commands()
            return False
        session = CommandSession(self, args)
        try:
            wrapper.command.execute(session)
        except CommandRunningError as err:
            print('error on command %s : %s' % (command, err))
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

