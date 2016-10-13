# -*- coding: utf-8 -*-


class Token(object):
    def __init__(self, type, value, line_number, start_at):
        self.type = type
        self.value = value
        self.line_number = line_number
        self.start_at = start_at

    def __repr__(self):
        return "<Token {}>".format(self.type)
