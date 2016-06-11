#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# jasily base.
# ----------

import os

def pip_require(module_name, pip_name=None):
    '''auto call `pip install` if module not install.'''
    try:
        __import__(module_name)
    except ImportError:
        if os.system('pip install ' + pip_name or module_name) != 0:
            raise ImportError('can not found module call ' + module_name)
