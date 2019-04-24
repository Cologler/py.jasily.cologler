#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.lang import switch

def test_switch_for():
    def switch_result(value):
        for case in switch(value):
            if case(1):
                return 1
            elif case(2):
                return 2
            else:
                return 3
    assert switch_result(1) == 1
    assert switch_result(2) == 2
    assert switch_result(4) == 3

def test_switch_with():
    def switch_result(value):
        with switch(value) as case:
            if case(1):
                return 1
            elif case(2):
                return 2
            else:
                return 3
    assert switch_result(1) == 1
    assert switch_result(2) == 2
    assert switch_result(4) == 3

def test_switch_chain():
    assert switch(1).case('A', 1).case('B', 2, 4).default('3') == 'A'
    assert switch(2).case('A', 1).case('B', 2, 4).default('3') == 'B'
    assert switch(3).case('A', 1).case('B', 2, 4).default('3') == '3'
    assert switch(4).case('A', 1).case('B', 2, 4).default('3') == 'B'
    assert switch(5).case('A', 1).case('B', 2, 4).default('3') == '3'
