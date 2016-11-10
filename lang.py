#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

# pylint: disable=C0103
# idea from https://code.activestate.com/recipes/410692/
class switch(object):
    """
    how to use `switch` ?
    ===
    for case in switch(name):
        if case('A'):
            pass
        elif case(1, 3):
            pass # for mulit-match.
        else:
            pass # for default.
    """
    def __init__(self, value):
        self._value = value
        self._exec = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if len(args) == 0:
            raise  SyntaxError('cannot match empty pattern.')
        if self._exec: # ready exec
            raise SyntaxError('cannot call match() after matched.')
        self._exec = self._value in args
        return self._exec
        