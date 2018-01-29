#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

# crc32
import binascii
import platform
# sha1
import hashlib

class HashCalculator:
    def __init__(self, path):
        self._path = path
        self._algorithms = {}
        self._value = {}

    def register_algorithm(self, algorithm):
        self._algorithms[algorithm.name] = algorithm

    def execute(self):
        if not self._algorithms:
            return
        for name in self._algorithms:
            self._value[name] = self._algorithms[name].init_value()
        blocksize = 1024 * 64
        with open(self._path, 'rb') as stream:
            while True:
                buffer = stream.read(blocksize)
                if len(buffer) == 0:
                    break
                for name in self._algorithms:
                    self._value[name] = self._algorithms[name].next_value(buffer, self._value[name])

    def get_result(self, name):
        ''' get result for name. '''
        return self._algorithms[name].to_string(self._value[name])

class HashAlgorithm:
    @property
    def name(self):
        ''' get algorithm name. '''
        raise NotImplementedError

    def init_value(self):
        ''' get algorithm init value. '''
        raise NotImplementedError

    def next_value(self, buffer, last_value):
        ''' get algorithm next value by buffer and last value. '''
        raise NotImplementedError

    def to_string(self, value):
        ''' convert value to upper string. '''
        return ("%08x" % value).upper()

    def compute_file(self, path):
        '''compute hash for file.'''
        with open(path, 'rb') as fp:
            return self.compute_stream(fp)

    def compute_stream(self, stream):
        '''compute hash for io object.'''
        value = self.init_value()
        while True:
            buffer = stream.read(1024 * 64)
            if not buffer:
                break
            value = self.next_value(buffer, value)
        return self.to_string(value)

    @classmethod
    def create(cls, name):
        name = name.lower()
        if name == 'crc32':
            return Crc32Algorithm()
        if name == 'sha1':
            return Sha1Algorithm()
        if name == 'md5':
            return Sha1Algorithm()
        alg = __HashlibHashAlgorithm.try_create(name)
        if not alg is None:
            return alg
        raise NotImplementedError

class Crc32Algorithm(HashAlgorithm):
    def __init__(self):
        py_ver = float(platform.python_version()[0])
        self.need_fix = py_ver < 3

    @property
    def name(self):
        return 'crc32'

    def init_value(self):
        return 0

    def next_value(self, buffer, last_value):
        crc = binascii.crc32(buffer, last_value)
        if self.need_fix:
            crc &= 0xffffffff
        return crc

class __HashlibHashAlgorithm(HashAlgorithm):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def init_value(self):
        return hashlib.new(self._name)

    def next_value(self, buffer, last_value):
        last_value.update(buffer)
        return last_value

    def to_string(self, value):
        return value.hexdigest().upper()

    @staticmethod
    def try_create(name):
        try:
            hashlib.new(name)
            return __HashlibHashAlgorithm(name)
        except ValueError:
            return None

class Sha1Algorithm(__HashlibHashAlgorithm):
    def __init__(self):
        super().__init__('sha1')

class Md5Algorithm(__HashlibHashAlgorithm):
    def __init__(self):
        super().__init__('md5')

if __name__ == '__main__':
    pass
