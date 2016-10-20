# -*- coding: utf-8 -*-
from elanus.parser import Parser, ParseException
from elanus.ast_node import *


def test_bind():
    def test(string, node):
        parse_result = Parser(string).parse()
        assert parse_result.expressions[0] == node

    test("\nlet foo = 1", Bind('foo', Int('1')))
    test("let foo = 1.1", Bind('foo', Float('1.1')))
    test("let foo = bar a 1", Bind('foo', Call("bar", ["a", Int("1")])))


def test_error():
    try:
        Parser("let foo = =").parse()
    except Exception as e:
        assert isinstance(e, ParseException)

    try:
        Parser("let foo = bar a =").parse()
    except Exception as e:
        assert isinstance(e, ParseException)
