#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import uuid

GUID_PY = 'py'
GUID_NET = '.net'


class Guid:
    def __init__(self, uid=None, mode=GUID_PY):
        if uid is None:
            uid = uuid.uuid4()
        elif isinstance(uid, str):
            uid = uuid.UUID(uid)
        assert isinstance(uid, uuid.UUID)
        assert mode in [GUID_PY, GUID_NET]
        self._uuid = uid
        self._mode = mode

    def __str__(self):
        return str(self._uuid)

    def to_string(self):
        '''str(self)'''
        return str(self)

    def convert_to_net(self):
        '''convert to .net style guid.'''
        if self._mode == GUID_NET:
            return self
        if self._mode == GUID_PY:
            value = str(self)
            converted = value[6:8] + value[4:6] + value[2:4] + value[0:2] +\
                        value[8] + value[11:13] + value[9:11] + value[13] +\
                        value[16:18] + value[14:16] + value[18:]
            return Guid(converted)
        raise NotImplementedError

    def convert_to_py(self):
        '''convert to python style guid.'''
        if self._mode == GUID_PY:
            return self
        if self._mode == GUID_NET:
            return Guid(self._uuid, GUID_PY).convert_to_net()
        raise NotImplementedError

