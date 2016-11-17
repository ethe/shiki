# -*- coding: utf-8 -*-
from .arithmetic import builtin as arithmetic_builtin
from .logical_oprations import builtin as logical_oprations_builtin


def builtin_init():
    environment = []
    environment.extend([(func.name, func) for func in arithmetic_builtin])
    environment.extend([(func.name, func) for func in logical_oprations_builtin])
    return environment
