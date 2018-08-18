# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# exitable mean some class has `__exit__(...)` attr.
# ----------

import sys
import atexit

def dispose_at_exit(exitable):
    '''
    register `exitable.__exit__()` into `atexit` module.

    return the `exitable` itself.
    '''
    @atexit.register
    def callback():
        exitable.__exit__(*sys.exc_info())
    return exitable
