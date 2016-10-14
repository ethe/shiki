# -*- coding: utf-8 -*-
from __future__ import print_function
from re import Scanner
from ast import literal_eval
from .token import *


class Lexer(object):
    def rules(self):
        result = [
            (r"\n",                                       self.newline),
            (r"\s+",                                      self.space),
            (r"\d+\.\d+",                                 self.float),
            (r"\d+",                                      self.int),
            (r"\+|-|\*|\/|=|==|>|<|\(|\)|\[|\]|\||,",     self.opration),
            (r"(let|func|do|end|return)\b",               self.keyword),
            (r"[a-zA-Z_][a-zA-Z_0-9]*(\?|!)?",            self.ident)
        ]
        return result

    def __init__(self, string):
        self.line, self.column = 1, 1
        scanner = Scanner(self.rules())
        self.result, self.remain = scanner.scan(string)
        if self.remain != '':
            print("Lexer error, can not lex {} at line {}, column {}".format(self.remain, self.line, self.column))

    macro = ("def {name}(self, _, value):\n"
             "    result = Token('{type}', value, self.line, self.column)\n"
             "    self.column += len(value)\n"
             "    return result")

    for type in ["NEWLINE", "SPACE", "FLOAT", "INT", "OPRATION", "IDENT", "KEYWORD"]:
        exec(macro.format(name=type.lower(), type=type))
