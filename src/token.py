# -*- coding: utf-8 -*-


class Token(object):
    def __init__(self, type, value='', line_number=0, start_at=0):
        self.type = type
        self.value = value
        self.line_number = line_number
        self.start_at = start_at

    def __eq__(self, another):
        return self.type == another.type

    def __repr__(self):
        return "<Token {}>".format(self.type)
