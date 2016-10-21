# -*- coding: utf-8 -*-
from .lexer import Lexer
from .ast_node import *


class Parser(Lexer):
    def parse(self):
        expressions = []
        line = self.line
        for token in self:
            if token.type == "SPACE" or token.type == "NEWLINE":
                continue
            expressions.append(self.parse_expression())
        return Expressions(expressions, line)

    def parse_expression(self):
        if self.word.value == "(":
            return self.parse_unit()
        elif self.word.value == "let":
            return self.parse_bind()
        elif self.word.type == "FLOAT":
            return self.parse_float()
        elif self.word.type == "INT":
            return self.parse_int()
        elif self.word.type == "IDENT":
            return self.parse_call()
        raise ParseExpressionException(self.line, self.column)

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
            self.skip_space()
            if self.word.type == "IDENT":
                args.append(self.word.value)
            elif self.word.type in ("FLOAT", "INT"):
                args.append(self.parse_expression())
            elif self.word.value == "(":
                args.append(self.parse_expression())
            elif self.word.value == ")":
                return Call(name=name, args=args)
            else:
                raise ParseCallException(self.line, self.column)
        return Call(name=name, args=args)

    def parse_unit(self):
        self.next()
        call = self.parse_expression()
        if not isinstance(call, Bind):
            self.assert_(")")
            return Unit(call)
        else:
            raise ParseUnitException(self.line, self.column)


class ParseException(Exception):
    def __init__(self, message, line, column):
        super(ParseException, self).__init__(
            "{message}, at line {line}, column {column}".format(message=message, line=line, column=column))


class ParseExpressionException(ParseException):
    def __init__(self, line, column):
        super(ParseExpressionException, self).__init__("Can not parse expression", line, column)


class ParseCallException(ParseException):
    def __init__(self, line, column):
        super(ParseCallException, self).__init__("Can not parse function call", line, column)


class ParseUnitException(ParseException):
    def __init__(self, line, column):
        super(ParseUnitException, self).__init__("Can not parse unit", line, column)
