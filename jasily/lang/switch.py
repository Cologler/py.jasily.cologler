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
    to use `switch`, here are some examples:

    ``` py
    # example 1:
    for case in switch(value):
        if case('A', 1):
            pass # value match any of ('A', 1)
        else:
            pass # for default.

    # example 2:
    with switch(value) as case:
        if case('A', 1):
            pass # value match any of ('A', 1)
        else:
            pass # for default.

    # example 3:
    ret = switch(2).case('A', 1).case('B', 2, 4).default(3)
    assert ret == 'B'
    ```

    """
    def __init__(self, value):
        self._value = value

    def __iter__(self):
        """ return the match method once for `for` stat. """
        yield self.match

    def __enter__(self):
        """ return the match method for `with` stat. """
        return self.match

    def __exit__(self, *args):
        pass

    @staticmethod
    def match_args(value, args):
        '''check whether the value match the pattern args.'''
        return value in args

    def match(self, *args):
        """
        Indicate whether or not to enter a case suite.

        usage:

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
        if not args:
            raise SyntaxError('cannot case empty pattern.')

        return self.match_args(self._value, args)

    def case(self, value, *args):
        if not args:
            raise SyntaxError('cannot case empty pattern.')

        test_value = self._value

        class ICase:
            def default(self, value):
                return value

        class Case(ICase):

            def case(self, value, *args):
                if not args:
                    raise SyntaxError('cannot case empty pattern.')

                if switch.match_args(test_value, args):
                    return ResultCase(value)
                else:
                    return CASE

        CASE = Case()

        class ResultCase(ICase):
            def __init__(self, value):
                self._value = value

            def case(self, value, *args):
                if not args:
                    raise SyntaxError('cannot case empty pattern.')

                return self

            def default(self, value):
                return self._value

        return CASE.case(value, *args)
