#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools
import threading

def _create_wrapper(func, factory, factory_args=[], factory_kwargs={}):
    sync = factory(*factory_args, **factory_kwargs)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sync:
            return func(*args, **kwargs)

    return wrapper

def lock(func):
    '''
    use `Lock` to keep func access thread-safety.

    example:

    ``` py
    @lock
    def func(): pass
    ```
    '''
    return _create_wrapper(func, threading.Lock)

def rlock(func):
    '''
    use `RLock` to keep func access thread-safety.

    example:

    ``` py
    @rlock
    def func(): pass
    ```
    '''
    return _create_wrapper(func, threading.RLock)

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

    def _wrap(func):
        return _create_wrapper(func, lock_type, factory_kwargs={'value': count})

    return _wrap


