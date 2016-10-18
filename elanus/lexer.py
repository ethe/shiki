# -*- coding: utf-8 -*-
from __future__ import print_function
from ast import literal_eval
from .scanner import StringScanner
from .token import *


class Lexer(StringScanner):
    def lexicon(self):
        return [
            ("newline",      r"\n"),
            ("space",        r"\s+"),
            ("float",        r"\d+\.\d+"),
            ("int",          r"\d+"),
            ("opration",     r"\+|-|\*|\/|=|==|>|<|\"|\'|\(|\)|\[|\]|\||,"),
            ("keyword",      r"(let|func|do|end|return)\b"),
            ("ident",        r"[a-zA-Z_][a-zA-Z_0-9]*(\?|!)?")
        ]

    def __init__(self, string):
        super(Lexer, self).__init__(string)
        self.line, self.column = 1, 1

    def newline(self, value):
        result = Token('NEWLINE', value, self.line, self.column)
        self.column = 1
        self.line += 1
        return result

    macro = ("def {name}(self, value):\n"
             "    result = Token('{type}', value, self.line, self.column)\n"
             "    self.column += len(value)\n"
             "    return result")

    for type in ["SPACE", "FLOAT", "INT", "OPRATION", "IDENT", "KEYWORD"]:
        exec(macro.format(name=type.lower(), type=type))

    def assert_(self, value):
        if self.word.value == value:
            return True
        raise BaseException()

    def assert_type_(self, type):
        if self.word.type == type:
            return True
        raise BaseException()

    def assert_next(self, value):
        if self.word.value == value:
            return self.next()
        raise BaseException()

    def assert_type_next(self, type):
        if self.word.type == type:
            return self.next()
        raise BaseException()
