#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

def assert_error(error_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as err:
        if not isinstance(err, error_type):
            raise
    else:
        raise AssertionError('should raise a %s' % error_type.__name__)
