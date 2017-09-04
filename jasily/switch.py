#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

# pylint: disable=C0111
def ensure_case(args):
    if not args:
        raise SyntaxError('cannot case empty pattern.')

# pylint: disable=C0103
# idea from https://code.activestate.com/recipes/410692/
class switch(object):
    """
    to use `switch`, here are examples:

    **example 1:**

    ``` py
    for case in switch(value):
        if case('A'):
            pass
        elif case(1, 3):
            pass # for mulit-match.
        else:
            pass # for default.
    ```

    **example 2:**

    ``` py
    ret = switch(2).case('A', 1).case('B', 2, 4).default(3).end()
    assert ret == 'B'
    ```

    """
    def __init__(self, value):
        self._value = value
        self._exec = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match

    def match(self, *args):
        """
        ``` py
        for case in switch(value):
            if case('A'):
                pass
            elif case(1, 3):
                pass # for mulit-match.
            else:
                pass # for default.
        ```
        """
        ensure_case(args)
        if self._exec: # ready exec
            raise SyntaxError('cannot call match() after matched.')
        self._exec = self._value in args
        return self._exec

    def case(self, value, *args):
        ensure_case(args)
        test_value = self._value

        class Default:
            def __init__(self, has_value: bool, value):
                self._has_value = has_value
                self._value = value

            def end(self):
                '''End the switcher.'''
                return self._value

        class Case(Default):
            def __init__(self, has_value: bool, value):
                '''
                args mode:

                if has_value is True:
                    value is finally value.
                else:

                '''
                self._has_value = has_value
                self._value = value

            def case(self, value, *args):
                ensure_case(args)
                if self._has_value:
                    return self
                else:
                    return Case(test_value in args, value)

            def default(self, value):
                ret_val = self._value if self._has_value else value
                return Default(True, ret_val)

        return Case(test_value in args, value)
