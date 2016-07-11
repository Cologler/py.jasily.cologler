#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# a `with statements` wrap for textwrap
# ----------

import textwrap
from contextlib import contextmanager

class _BaseTextWrapper:
    def __init__(self):
        self.predicate = None

    def wrap_text(self, text):
        if self.predicate is None or self.predicate(text):
            return self._wrap_core(text)
        else:
            return text

    def _wrap_core(self, text): raise NotImplementedError

class _BasicTextWrapper(_BaseTextWrapper):
    def _wrap_core(self, text):
        return text

class TextPrinter:
    '''a [with statement]s wrap for textwrap'''
    def __init__(self):
        self._wrappers = [_BasicTextWrapper()]
        
        printer = self

        class Releaser:
            def __enter__(self):
                return printer
            def __exit__(self, *args):
                printer._wrappers.pop()

        self._releaser = Releaser()

    def __enter(self, wrapper):
        self._wrappers.append(wrapper)
        return self._releaser

    def print(self, text):        
        wrappers = self._wrappers.copy()
        while len(wrappers) > 0:
            text = wrappers.pop().wrap_text(text)
        print(text)

    def indent(self, prefix, predicate=None):

        class _IndentTextWrapper(_BaseTextWrapper):
            def __init__(self, prefix):
                super().__init__()
                self._prefix = prefix
            def _wrap_core(self, text):
                return textwrap.indent(text, self._prefix, predicate=self.predicate)
        
        wrapper = _IndentTextWrapper(prefix)
        wrapper.predicate = predicate
        return self.__enter(wrapper)