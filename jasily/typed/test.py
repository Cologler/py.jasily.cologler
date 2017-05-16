#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections import Iterable
from inspect import signature


def is_iterable(obj):
    return isinstance(obj, Iterable)


