#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools
import threading

from ..lang import with_it


def lock(func):
    '''
    use `Lock` to keep func access thread-safety.

    example:

    ``` py
    @lock
    def func(): pass
    ```
    '''

    return with_it(threading.Lock())(func)


def rlock(func):
    '''
    use `RLock` to keep func access thread-safety.

    example:

    ``` py
    @rlock
    def func(): pass
    ```
    '''

    return with_it(threading.RLock())(func)


def semaphore(count: int, bounded: bool=False):
    '''
    use `Semaphore` to keep func access thread-safety.

    example:

    ``` py
    @semaphore(3)
    def func(): pass
    ```
    '''

    lock_type = threading.BoundedSemaphore if bounded else threading.Semaphore
    lock_obj = lock_type(value=count)

    return with_it(lock_obj)
