#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import os

def descriptor(func):
    doc = '[Descriptor]\n' + (func.__doc__ or '')
    func.__doc__ = doc
    return func

