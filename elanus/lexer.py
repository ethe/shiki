# -*- coding: utf-8 -*-
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
            ("keyword",      r"(let|func|do|end|return|and|or|not|true|false)\b"),
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

    def assert_(self, *value):
        if self.word.value in value:
            return True
        raise TokenAssertException(self.line, self.column)

    def assert_type_(self, *type):
        if self.word.type in type:
            return True
        raise TokenAssertException(self.line, self.column)

    def assert_and_next(self, *value):
        if self.assert_(*value):
            return self.next()

    def assert_type_and_next(self, *type):
        if self.assert_type_(*type):
            return self.next()

    def skip_space_and_assert(self, *value):
        self.assert_type_and_next("SPACE")
        return self.assert_(*value)

    def skip_space_and_assert_type(self, *type):
        self.assert_type_and_next("SPACE")
        return self.assert_type_(*type)

    def skip_space(self):
        if self.word.type == "SPACE":
            self.next()

    def safe_next(self):
        if not self.eof():
            self.next()
        else:
            raise TokenAssertException(self.line, self.column)


class TokenAssertException(Exception):
    def __init__(self, line, column):
        super(TokenAssertException, self).__init__(
            "Find unexpected token, at line {line}, column {column}".format(line=line, column=column))
