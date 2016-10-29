# -*- coding: utf-8 -*-
def trampoline(f, *args, **kwargs):
    def trampolined_f(*args, **kwargs):
        result = f(*args, **kwargs)
        while callable(result):
            result = result()
        return result
    return trampolined_f
