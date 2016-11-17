# -*- coding: utf-8 -*-
from .arithmetic import builtin


def builtin_init():
    environment = []
    environment.extend([(func.name, func) for func in builtin])
    return environment
