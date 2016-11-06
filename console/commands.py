#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import inspect

from .. import check_arguments
from ..convert import StringConverter
from ..convert import ConvertError
from ..text import TextPrinter
from . import ConsoleArguments


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


class CommandParameter:
    @check_arguments
    def __init__(self, parameter: inspect.Parameter):
        self._parameter = parameter
        self.desc = ''

    @property
    def name(self):
        return self._parameter.name

class CommandParameters:
    def __init__(self, func):
        self._parameters = []
        self._parameters_map = {}

        sign = inspect.signature(func)
        for parameter in sign.parameters.values():
            self.__add(CommandParameter(parameter))

    def __getitem__(self, key: str) -> CommandParameter:
        return self._parameters_map[key]

    def __add(self, parameter: CommandParameter):
        self._parameters.append(parameter)
        self._parameters_map[parameter.name] = parameter


class CommandDefinition():
    def __init__(self, func, alias):
        self._desc = func.__doc__ or '%s command.' % func.__name__
        self._func = func
        self._command_alias = alias
        self._enable_sorted_args = False

        '''set() for args name. is useful for check if arg is exists.'''
        self._args_name = set()
        self._args_alias = {}
        self._converter = StringConverter()
        self._parameters = CommandParameters(func)

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
            for arg in args:
                self._args_name.add(arg)
        else:
            raise CommandDefinitionError('command cannot contains varargs or varkeywords')

    def __str__(self):
        return self.name

    @property
    def name(self):
        '''get command name.'''
        return self._func.__name__.replace('_', '-')

    def names(self):
        '''yield command name and alias.'''
        yield self.name
        for name in self.command_alias:
            yield name

    @property
    def desc(self) -> str:
        return self._desc

    @desc.setter
    @check_arguments
    def desc(self, value: str):
        self._desc = value

    @property
    def command_alias(self):
        '''get command alias.'''
        return self._command_alias

    ########################## arg ##########################

    @check_arguments
    def arg_add_alias(self, arg: str, alias: str):
        assert isinstance(alias, str)
        self._parameters[arg]
        self._args_alias.setdefault(arg, []).append(alias)

    @check_arguments
    def arg_set_desc(self, arg: str, desc: str):
        self._parameters[arg].desc = desc

    def arg_get_desc(self, arg):
        return self._parameters[arg].desc

    @property
    def func(self):
        '''get command func pointer.'''
        return self._func

    @property
    def require_args(self):
        '''get require args.'''
        return self._require_args[1:]

    @property
    def optional_args(self):
        '''get optional args.'''
        return list(self._optional_args)

    def enable_sorted_args(self):
        self._enable_sorted_args = True

    def execute(self, session):
        '''execute command. possible raise CommandRunningError.'''

        # pre args
        assert isinstance(session, CommandSession)
        require_args = self.require_args
        optional_args = self._optional_args

        # converter
        def arg_convert(arg_name, arg_val, arg_defval):
            '''convert arg type.'''
            if arg_val == arg_defval:
                return arg_val
            if isinstance(arg_val, type(arg_defval)):
                return arg_val
            if isinstance(arg_defval, int) or isinstance(arg_defval, float):
                try:
                    return self._converter.to(type(arg_defval), arg_val)
                except ConvertError:
                    raise CommandRunningError('arg %s should be digit.' % arg_name)
            return arg_val

        # arg func
        def get_unique_key(key):
            '''return None if key not found.'''
            exists_key = key if key in session.args else None
            if key in self._args_alias:
                for alias in self._args_alias[key]:
                    if alias in session.args:
                        if exists_key is None:
                            exists_key = alias
                        else:
                            raise CommandRunningError('conflict arg flag: %s and %s' % \
                                (exists_key, alias))
            return exists_key

        def append_optional_args(count=None):
            for arg in optional_args:
                arg_name, arg_defval = arg
                exists_key = get_unique_key(arg_name)
                if exists_key is None:
                    arg_val = arg_defval
                else:
                    arg_val = session.args.get(exists_key)
                    arg_val = arg_convert(arg_name, arg_val, arg_defval)
                    if count != None:
                        count -= 1
                exe_args.append((arg[0], arg_val))
            if count != None and count != 0:
                raise CommandRunningError('command contain unknown args.')

        exe_args = []
        exe_args.append((self._require_args[0], session))

        if self._enable_sorted_args:
            args_inputed = list(session.args)[2:]
            compared = len(require_args) - len(args_inputed)
            if compared > 0:
                missing = [x.upper() for x in require_args[-compared:]]
                print('error on command %s : missing argument (%s)' %\
                    (self.name, ','.join(missing)))
                return
            elif compared < 0:
                # require args
                for arg_name, arg_value in list(zip(require_args, args_inputed[-len(require_args):])):
                    exe_args.append((arg_name, arg_value))
                # optional args
                append_optional_args(count=0-compared)
            else:
                for arg_name, arg_value in list(zip(require_args, args_inputed)):
                    exe_args.append((arg_name, arg_value))
        else:
            for key in require_args:
                arg_name = get_unique_key(key)
                if arg_name is None:
                    print('missing argument on command %s : %s' % (self.name, arg_name))
                    return
                else:
                    exe_args.append((arg_name, session.args.get_or_error(key)))
            append_optional_args()
        self.func(**dict(exe_args))

def arg_alias(**args):
    '''add arg alias to command.'''
    def wrap(cmd: CommandDefinition):
        for arg in args:
            val = args[arg]
            if isinstance(val, str):
                cmd.arg_add_alias(arg, val)
            elif isinstance(val, list):
                for x in val:
                    cmd.arg_add_alias(arg, x)
            else:
                raise TypeError
        return cmd
    return wrap

def arg_desc(**args):
    '''add arg desc to command.'''
    def wrap(cmd: CommandDefinition):
        for arg in args:
            cmd.arg_set_desc(arg, args[arg])
        return cmd
    return wrap

def enable_sorted_args(cmd: CommandDefinition):
    '''
    if enable, will pass require args with sorted and ignore arg name.
    all optional args should before require args by input.
    the input format will be 'cmd -a -b value1 value2'.
    '''
    cmd.enable_sorted_args()
    return cmd

def desc(value):
    '''set desc to command.'''
    def wrap(cmd: CommandDefinition):
        cmd.desc = value
        return cmd
    return wrap

def command(alias=[]):
    '''make a func to a CommandDefinition object. you can manual call func by func property.'''
    def wrap(func):
        return CommandDefinition(func, alias)
    return wrap

class _CommandWrapper:
    def __init__(self, cmd):
        self.command = cmd
        self.is_enable = True

class CommandSession:
    '''session info of @command'''
    def __init__(self, manager, args: ConsoleArguments, **env):
        assert isinstance(manager, CommandManager)
        assert isinstance(args, ConsoleArguments)
        self._manager = manager
        self._args = args
        self._env = env

    @property
    def command_manager(self):
        '''get caller CommandManager object.'''
        return self._manager

    @property
    def args(self) -> ConsoleArguments:
        '''get args parser for this session.'''
        return self._args

    @property
    def command(self) -> str:
        '''get command text which route to current command.'''
        return self._args[1]

    @property
    def env(self):
        '''get session env dict.'''
        return self._env

    def print_command(self):
        self._manager.print_command(self._manager.get_command(self.command))

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

    def command(self, alias=[]):
        '''
        create and register command.
        if have a lot command(), only first alias will work.
        '''
        def wrap(func):
            if isinstance(func, CommandDefinition):
                cmd = func
            else:
                cmd = command(alias)(func)
            self.register(cmd)
            return cmd
        return wrap

    def get_command(self, cmd_key, show_help=True):
        wrapper = self._commands_mapper.get(cmd_key)
        if wrapper is None:
            if show_help:
                print('unknown command: ' + cmd_key)
                self.print_commands()
            return None
        return wrapper.command

    def execute(self, argv, **env):
        '''execute command by argv.'''
        args = ConsoleArguments(argv)
        if len(args) < 2:
            print('missing command')
            self.print_commands()
            return False
        cmd = self.get_command(args[1])
        if cmd is None: return
        session = CommandSession(self, args, **env)
        try:
            cmd.execute(session)
        except CommandRunningError as err:
            session.print_command()
            print('error on command %s : %s' % (cmd.name, err))
        return True

    def print_command(self, cmd, indent=0):
        FIELD_INDENT = 15
        printer = TextPrinter()

        def alias_of_arg(name):
            yield name
            if name in cmd._args_alias:
                for a in cmd._args_alias[name]:
                    yield a

        def arg_format(name, defval=None):
            formated = '-' + '|'.join(alias_of_arg(name))
            if not defval is None:
                if type(defval) != bool:
                    formated += '=%s' % defval
                formated = '[%s]' % formated
            return formated

        def print_optional():
            if len(cmd.optional_args) > 0:
                with printer.indent_inc('', 'options:', FIELD_INDENT):
                    for n, v in cmd.optional_args:
                        adef = arg_format(n, v)
                        desc = cmd.arg_get_desc(n)
                        if desc != '':
                            printer.print(adef + '   ' + desc)
                        else:
                            printer.print(adef)
                        #printer.print(adef + cmd.arg_get_desc(n))
        with printer.indent_inc(' ' * indent):
            printer.print(cmd.name)
            with printer.indent_inc(' ' * 3):
                printer.print(cmd.desc)
                with printer.indent_inc(' ' * 5):
                    cmd_format_array = [cmd.name]
                    if len(cmd.require_args) + len(cmd.optional_args) > 0:
                        if not cmd._enable_sorted_args:
                            if len(cmd.require_args) > 0:
                                with printer.indent_inc('', 'requires:', FIELD_INDENT):
                                    requires = ['[-%s]' % '|'.join(alias_of_arg(n)) for n in cmd.require_args]
                                    requires = ' '.join(requires)
                                    printer.print(requires)
                        optionals_array = []
                        if len(cmd.optional_args) > 0:
                            optionals_array = [arg_format(n, v) for n, v in cmd.optional_args]
                            cmd_format_array += optionals_array
                        if cmd._enable_sorted_args:
                            requires_array = [x.upper() for x in cmd.require_args]
                            cmd_format_array += requires_array
                        print_optional()
                    with printer.indent_inc('', 'format:', FIELD_INDENT):
                        printer.print(' '.join(cmd_format_array))
                    if len(cmd.command_alias) > 0:
                        with printer.indent_inc('', 'alias:', FIELD_INDENT):
                            printer.print(', '.join(cmd.command_alias))

    def print_commands(self):
        print('usage:')
        for cmd in [x.command for x in self._commands if x.is_enable]:
            self.print_command(cmd, 3)
            print()

