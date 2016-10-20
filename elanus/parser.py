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
        raise ParseException(self.line, self.column)

    def parse_int(self):
        result = Int(self.word.value, self.line)
        return result

    def parse_float(self):
        result = Float(self.word.value, self.line)
        return result

    def parse_bind(self):
        self.next()
        self.skip_space_and_assert_type("IDENT")
        name = self.word.value
        self.next()
        self.skip_space_and_assert("=")
        self.next()
        self.assert_type_and_next("SPACE")
        value = self.parse_expression()
        return Bind(name, value, self.line)

    def parse_call(self):
        name = self.word.value
        args = []
        while not self.eof():
            self.next()
            self.assert_type_and_next("SPACE")
            if self.word.type == "IDENT":
                args.append(self.word.value)
            elif self.word.type in ("FLOAT", "INT"):
                args.append(self.parse_expression())
            else:
                raise ParseException(self.line, self.column)
        return Call(name=name, args=args)


class ParseException(Exception):
    def __init__(self, line, column):
        super(ParseException, self).__init__(
            "Can not parse expression, at line {line}, column {column}".format(line=line, column=column))
