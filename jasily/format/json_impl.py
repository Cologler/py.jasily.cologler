#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json

class JsonSerializer:

    def serialize(self, obj):
        d = self.__serialize_value(obj)
        return json.dumps(d, indent=2)

    def __serialize_value(self, v):
        if isinstance(v, dict):
            return self.__serialize_dict(v)
        elif isinstance(v, (int, float, list, bool)):
            return v
        else:
            return self.__serialize_dict(v.__dict__)

    def __serialize_dict(self, d: dict):
        dc = d.copy()
        for k in d:
            if not k.startswith('_'):
                v = d[k]
                dc[k] = self.__serialize_value(v)
        return dc

    def deserialize(self, cls: type, s: str):
        obj = cls()
        self.__merge_dict(obj.__dict__, json.loads(s))
        return obj

    def __merge_dict(self, to_dict: dict, from_dict: dict):
        for k in from_dict:
            self.__deserialize_obj_value(to_dict, from_dict, k)

    def __deserialize_obj_value(self, to_dict: dict, from_dict: dict, k):
        fv = from_dict[k]
        tv = to_dict.get(k)
        if isinstance(fv, dict) and isinstance(tv, dict):
            self.__merge_dict(tv, fv)
        else:
            to_dict[k] = fv
