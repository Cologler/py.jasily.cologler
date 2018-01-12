#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

UNIT_BYTES = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB')


def format_size(size: int) -> str:
    '''
    get formated size.

    example:
    ``` py
    format_size(10000000) # 9.537 MB
    ```
    '''
    level = 0
    while size > 1024:
        size /= 1024
        level += 1
    return '%.3f %s' % (size, UNIT_BYTES[level])
