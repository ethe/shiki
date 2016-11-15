# -*- coding: utf-8 -*-
from __future__ import print_function


def trace(value):
    if isinstance(value, tuple):
        value = value[1]
    print(value)
    return value
