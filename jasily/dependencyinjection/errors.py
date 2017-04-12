#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class InjectError(Exception):
    '''raise when error from dependency injection module.'''

class TypeNotFoundError(InjectError):
    '''raise when user want to inject type which is not provided.'''
