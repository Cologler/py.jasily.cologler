#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from ..exceptions import JasilyBaseException, MessageException


class CliException(MessageException):
    pass


class ParameterException(CliException):
    pass


class NameConflictException(CliException):
    def __init__(self, name: str, message: str):
        super().__init__(message, name=name)

