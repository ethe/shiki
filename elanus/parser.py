# -*- coding: utf-8 -*-
from .lexer import Lexer
from .ast_node import *


class Parser(Lexer):
    def parse(self):
        self.next()
        while self.word.type in ("SPACE", "NEWLINE"):
            self.next()
        return self.parse_expressions()

    def parse_expressions(self, inside=False):
        line = self.line
        expressions = []
        while not self.eof() and self.word.value != "end":
            expressions.append(self.parse_expression(inside=inside))
            if self.eof() or self.word.value == "end":
                break
            self.safe_next()
            while self.word.type in ("NEWLINE", "SPACE"):
                self.safe_next()
        return Expressions(expressions, line)

    def parse_expression(self, inside=False):
        self.skip_space()
        if self.word.value == "(":
            return self.parse_unit()
        elif self.word.value == ")":
            return self.parse_void()
        elif self.word.value == "let":
            return self.parse_bind()
        elif self.word.value == "func":
            return self.parse_function()
        elif self.word.value == "return":
            return self.parse_return(inside=inside)
        elif self.word.type == "FLOAT":
            return self.parse_float()
        elif self.word.type == "INT":
            return self.parse_int()
        elif self.word.type == "IDENT" or self.word.value in ("+", "-", "*", "/"):
            return self.parse_call()
        raise ParseExpressionException(self.line, self.column)

    def parse_int(self):
        result = Int(self.word.value, self.line)
        self.safe_next()
        return result

    def parse_float(self):
        result = Float(self.word.value, self.line)
        self.safe_next()
        return result

    def parse_bind(self):
        self.safe_next()
        self.skip_space_and_assert_type("IDENT")
        name = self.word.value
        self.safe_next()
        self.skip_space_and_assert("=")
        self.safe_next()
        self.assert_type_and_next("SPACE")
        value = self.parse_expression()
        return Bind(name, value, self.line)

    def parse_call(self):
        name = self.word.value
        args = []
        self.safe_next()
        while True:
            self.skip_space()
            if self.word.type == "IDENT":
                args.append(self.word.value)
                self.safe_next()
            elif self.word.type in ("FLOAT", "INT") or self.word.value == "(":
                args.append(self.parse_expression())
            elif self.word.value in (")", "end", "\n") or self.eof():
                break
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

    def parse_function(self):
        line = self.line
        if not self.eof():
            args = []
            self.safe_next()
            self.skip_space_and_assert_type("IDENT")
            name = self.word.value
            self.safe_next()
            self.assert_type_and_next("SPACE")
            while self.word.value != "do":
                if self.word.type == "IDENT":
                    args.append(self.word.value)
                    self.safe_next()
                    self.assert_type_and_next("SPACE")
                else:
                    raise ParseFunctionException(self.line, self.column)
            self.safe_next()
            self.assert_type_and_next("SPACE", "NEWLINE")
            expressions = self.parse_expressions(inside=True)
            self.skip_space()
            self.assert_and_next("end")
            return Function(name, args, expressions, line)
        else:
            raise ParseFunctionException(self.line, self.column)

    def parse_return(self, inside):
        line, column = self.line, self.column
        self.safe_next()
        if inside:
            expression = self.parse_expression()
            if isinstance(expression, Bind):
                raise ParseReturnException("Binding does not have a return", line, column)
            return Return(expression, line)
        else:
            raise ParseReturnException("Return outside function", line, column)

    def parse_void(self):
        return Void(self.line)


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


class ParseFunctionException(ParseException):
    def __init__(self, line, column):
        super(ParseFunctionException, self).__init__("Can not parse function", line, column)


class ParseReturnException(ParseException):
    def __init__(self, message, line, column):
        super(ParseReturnException, self).__init__(message, line, column)
