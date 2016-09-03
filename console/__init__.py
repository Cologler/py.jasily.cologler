#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import re
import sys

class _UnbufferedStream(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def stdout_disable_buffer():
    '''disable buffer for stdout.'''
    stream = sys.stdout
    if stream is None:
        return
    if not isinstance(stream, _UnbufferedStream):
        sys.stdout = _UnbufferedStream(stream)

def stdout_enable_buffer():
    '''enable buffer for stdout.'''
    stream = sys.stdout
    if stream is None:
        return
    if isinstance(stream, _UnbufferedStream):
        sys.stdout = stream.stream

class MissingArgumentError(Exception):
    ''' missing argument. '''
    def __init__(self, argument_name):
        super().__init__()
        self._argument_name = argument_name

    def __str__(self):
        return 'missing argument ' + self._argument_name

class ConsoleArguments:
    '''parse command arguments'''
    mode = re.compile(r'^--?([^-=]+)(?:[:=]([^=]*))?$')

    def __init__(self, argv):
        assert isinstance(argv, list)
        self._argv = argv
        self._parsed_argv = []
        self._non_parsed_argv = []
        self._keys = set()
        for arg in argv:
            self.__parse_arg(arg)
        assert len(self._parsed_argv) + len(self._non_parsed_argv) == len(self._argv)

    def __parse_arg(self, arg):
        assert isinstance(arg, str)
        if len(arg) > 0:
            if arg[0] == '"':
                if arg[-1] == '"':
                    arg = arg[1:-1]
                else:
                    arg = arg[1:]
        match = self.mode.match(arg)
        if not match is None:
            groups = match.groups()
            self._parsed_argv.append(groups)
            self._keys.add(groups[0])
        else:
            self._non_parsed_argv.append(arg)

    def __len__(self):
        '''return len of original argv.'''
        return len(self._argv)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._argv[index]
        elif isinstance(index, str):
            return self.get_or_error(index)

    def __iter__(self):
        return self._argv.__iter__()

    def __contains__(self, key):
        return key in self._keys

    def non_parsed_argv(self):
        return self._non_parsed_argv.__iter__()

    def get(self, key, default=None):
        '''get argument value by key. if not found, return default value.
           if arg is flag like '-v', it will return a boolean True.'''
        assert isinstance(key, str)
        for item in self._parsed_argv:
            if isinstance(item, tuple):
                if item[0] == key:
                    return item[1] if not item[1] is None else True
        return default

    def get_or_error(self, key):
        ''' get argument value by key. if not found, raise MissingArgumentError. '''
        assert isinstance(key, str)
        ret = self.get(key, None)
        if ret is None:
            raise MissingArgumentError(key)
        else:
            return ret

    def keys(self):
        for item in self._keys:
            yield item

    def values(self):
        for item in self._parsed_argv:
            if isinstance(item, tuple):
                yield item[1]

if __name__ == '__main__':
    assert ConsoleArguments(['"-av=1d"']).get('av') == '1d'
