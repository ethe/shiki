# -*- coding: utf-8 -*-
from .lexer import Lexer
from .ast_node import *


class Parser(Lexer):
    def parse(self):
        expressions = []
        for token in self:
            if token.type == "SPACE" or token.type == "NEWLINE":
                continue
            expressions.append(self.parse_expression())
        return Expressions(expressions)

    def parse_expression(self):
        if self.word.value == "let":
            return self.parse_bind()
        elif self.word.type == "FLOAT":
            return self.parse_float()
        elif self.word.type == "INT":
            return self.parse_int()
        elif self.word.type == "IDENT":
            return self.parse_call()

    def parse_int(self):
        result = Int(self.word.value, self.line)
        return result

    def parse_float(self):
        result = Float(self.word.value, self.line)
        return result

    def parse_bind(self):
        self.assert_next("let")
        self.assert_type_next("SPACE")
        self.assert_type_("IDENT")
        name = self.word.value
        self.next()
        self.assert_type_next("SPACE")
        self.assert_next("=")
        self.assert_type_next("SPACE")
        value = self.parse_expression()
        return Bind(name, value, self.line)
