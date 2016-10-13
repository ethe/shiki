# -*- coding: utf-8 -*-
from __future__ import print_function
from re import Scanner
from ast import literal_eval
from .token import *


class Lexer(object):
    def rules(self):
        result = [
            (r"\n", self.newline),
            (r"\s+", self.space),
            (r"\d+\.\d+", self.float),
            (r"\d+", self.int),
            (r"\+|-|\*|\/", self.opration),
            (r"[a-zA-Z_][a-zA-Z_0-9]*(\?|!)?", self.ident)
        ]
        return result

    def __init__(self, string):
        self.line, self.column = 1, 1
        scanner = Scanner(self.rules())
        self.result, self.remain = scanner.scan(string)
        if self.remain != '':
            print("Lexer error, can not lex {} at line {}, column {}".format(self.remain, self.line, self.column))

    def newline(self, _, value):
        result = Token('NEWLINE', value, self.line, self.column)
        self.line += 1
        self.column = 1
        return result

    def space(self, _, value):
        result = Token('SPACE', value, self.line, self.column)
        self.column += len(value)
        return result

    def float(self, _, value):
        result = Token('FLOAT', value, self.line, self.column)
        self.column += len(value)
        return result

    def int(self, _, value):
        result = Token('INT', value, self.line, self.column)
        self.column += len(value)
        return result

    def opration(self, _, value):
        result = Token('OPRATION', value, self.line, self.column)
        self.column += len(value)
        return result

    def ident(self, _, value):
        result = Token('IDENT', value, self.line, self.column)
        self.column += len(value)
        return result
