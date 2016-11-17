# -*- coding: utf-8 -*-
class Singleton(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        cls.instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.instance
