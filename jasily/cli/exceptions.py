#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class CliException(Exception):
    def __init__(self, message: str):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class UserInputException(CliException):
    '''raise when user input cannot pass to command.'''
    pass


class ApplicationException(CliException):
    '''
    raise when the application has error code.
    this should only happen when you debug the cli.
    '''
    pass


class RuntimeException(CliException):
    '''
    raise when application execute has error.
    '''
    pass
