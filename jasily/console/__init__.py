#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import re

class ArgumentsParser:
    mode = re.compile(r'^--?([^-=]+)(?:[:=]([^=]*))?$')

    def __init__(self, argv):
        assert isinstance(argv, list)
        self._argv = argv
        self._parsed_argv = []
        for arg in argv:
            self._parse(arg)

    def _parse(self, arg):
        assert isinstance(arg, str)
        assert len(arg) > 0
        if arg[0] == '"':
            if arg[-1] == '"':
                arg = arg[1:-1]
            else:
                arg = arg[1:]
        match = self.mode.match(arg)
        if not match is None:
            groups = match.groups()
            self._parsed_argv.append(groups)

    def __iter__(self):
        return self.keys()

    def __contains__(self, key):
        for item in self.keys():
            if item == key:
                return True
        return False

    def get(self, key, default=None):
        for item in self._parsed_argv:
            if isinstance(item, tuple):
                if item[0] == key:
                    return item[1]
        return default

    def keys(self):
        for item in self._parsed_argv:
            if isinstance(item, tuple):
                yield item[0]
            else:
                yield item

    def values(self):
        for item in self._parsed_argv:
            if isinstance(item, tuple):
                yield item[1]

if __name__ == '__main__':
    assert ArgumentsParser(['"-av=1d"']).get('av') == '1d'
