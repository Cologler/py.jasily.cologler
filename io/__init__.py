#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import os

UNIT_BYTES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']

class FileSystem:
    ''' base class for Directory and File. '''
    def __init__(self, path):
        self._path = path if isinstance(path, Path) else Path(path)

    def __str__(self):
        return str(self._path)

    @property
    def path(self):
        ''' return a Path object. '''
        return self._path

    def hardlink(self, dest):
        ''' hard link item to dest path. '''
        raise NotImplementedError

    def is_exists(self):
        ''' check if this was exists. '''
        raise NotImplementedError

    def is_directory(self):
        ''' check if this is a exists directory. '''
        return False

    def is_file(self):
        ''' check if this is a exists file. '''
        return False

    @classmethod
    def from_path(cls, path):
        '''create instance from path.'''
        if os.path.isdir(path):
            return Directory(path)
        elif os.path.isfile(path):
            return File(path)
        else:
            return None

    def rename_without_extension(self, name):
        '''rename this item without extension.'''
        path = self.path.rename_without_extension(name)
        if self._path.path == path.path:
            return
        os.rename(self.path.path, path.path)
        self._path = path

    def rename(self, name):
        '''rename this item.'''
        path = self.path.rename(name)
        if self._path.path == path.path:
            return
        os.rename(self.path.path, path.path)
        self._path = path

    def get_normal_name(self):
        '''get normal name for item.
           for folder, return full name;
           for file, return name without extension.'''
        raise NotImplementedError

    def rename_normal(self, name):
        '''normal rename name for item.
           for folder, rename full name;
           for file, rename name without extension.'''
        raise NotImplementedError

    def move_to(self, dest_dir):
        if isinstance(dest_dir, Directory):
            dest_dir = dest_dir.path.path
        assert isinstance(dest_dir, str)
        new_path = Path(os.path.join(dest_dir, self.path.name))
        os.rename(self.path.path, new_path.path)
        self._path = new_path

class Directory(FileSystem):
    ''' Directory object. '''
    def __init__(self, path):
        super().__init__(path)

    def enumerate_items(self, include_file=True, include_dir=True):
        ''' get items from directory. '''
        for name in os.listdir(self.path.path):
            path = os.path.join(self.path.path, name)
            if os.path.isfile(path):
                if include_file:
                    yield File(path)
            elif os.path.isdir(path):
                if include_dir:
                    yield Directory(path)

    def enumerate_files(self):
        ''' get files from directory. '''
        return self.enumerate_items(include_dir=False)

    def enumerate_dirs(self):
        ''' get directorys from directory. '''
        return self.enumerate_items(include_file=False)

    def hardlink(self, dest):
        if isinstance(dest, Path):
            dest = dest.path
        assert isinstance(dest, str)
        mode = os.stat(self.path.path).st_mode
        # self
        if not os.path.isdir(dest):
            os.mkdir(dest)
        os.chmod(dest, mode)
        # child
        for item in self.enumerate_items():
            item.hardlink(os.path.join(dest, item.path.name))

    def is_exists(self):
        return os.path.isdir(self.path.path)

    def is_directory(self):
        ''' check if this is a exists directory. '''
        return self.is_exists()

    def get_normal_name(self):
        return self.path.name

    def rename_normal(self, name):
        self.rename(name)

def format_size(size):
    level = 0
    while size > 1024:
        size /= 1024
        level += 1
    return '%.3f %s' % (size, UNIT_BYTES[level])

class File(FileSystem):
    ''' File object. '''
    def __init__(self, path):
        super().__init__(path)

    @property
    def size(self):
        return os.path.getsize(self._path.path)

    def format_size(self):
        return format_size(self.size)

    def hardlink(self, dest):
        if isinstance(dest, Path):
            dest = dest.path
        assert isinstance(dest, str)
        os.link(self._path.path, dest)

    def is_exists(self):
        return os.path.isfile(self.path.path)

    def is_file(self):
        return self.is_exists()

    def get_normal_name(self):
        return self.path.name_without_extension

    def rename_normal(self, name):
        path = self.path.rename_without_extension(name)
        if self._path.path == path.path:
            return
        os.rename(self.path.path, path.path)
        self._path = path

class Path:
    ''' a immutable path wrapper. '''
    def __init__(self, path):
        assert isinstance(path, str)
        self._path = path
        self._dirname, self._name = os.path.split(path)
        self._name_without_extension, self._extension = os.path.splitext(self._name)

    def __str__(self):
        return self.path

    @property
    def path(self):
        ''' get string value for current path. '''
        return self._path

    @property
    def dirname(self):
        ''' get directory path from path. '''
        return self._dirname

    @property
    def name(self):
        ''' get name from path. '''
        return self._name

    @property
    def name_without_extension(self):
        return self._name_without_extension

    @property
    def extension(self):
        return self._extension

    def is_extension_equals(self, other):
        return self.extension.lower() == other.lower()

    def rename(self, name):
        path = os.path.join(self._dirname, name)
        return Path(path)

    def rename_without_extension(self, name):
        path = os.path.join(self._dirname, name + self._extension)
        return Path(path)

    def rename_extension(self, extension):
        if not extension.startswith('.'):
            extension = '.' + extension
        path = os.path.join(self._dirname, self.name_without_extension + extension)
        return Path(path)

