# -*- coding: utf-8 -*-
from .arithmetic import arithmetic


def is_builtin(call):
    if hasattr(call, "name"):
        return call.name in ['+', '-', '*', '/']
    return False


def builtin_victor(*args, **kwargs):
    if call.name in ['+', '-', '*', '/']:
        return arithmetic(args[0], args[1], args[2])
