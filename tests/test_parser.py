# -*- coding: utf-8 -*-
from elanus.parser import *
from elanus.ast_node import *


def test_bind():
    def test(string, node):
        parse_result = Parser(string).parse()
        assert parse_result == Expressions([node])

    test("\nlet foo = 1", Bind('foo', Int('1')))
    test("let foo = 1.1", Bind('foo', Float('1.1')))
    test("let foo = bar a 1", Bind('foo', Call("bar", ["a", Int("1")])))


def test_unit():
    expressions = Parser("foo bar (test 1 2)").parse()
    assert expressions == Expressions([Call("foo", ["bar", Unit(Call("test", [Int("1"), Int("2")]))])])


def test_error():
    try:
        Parser("let foo = =").parse()
    except Exception as e:
        assert isinstance(e, ParseExpressionException)

    try:
        Parser("let foo = bar a =").parse()
    except Exception as e:
        assert isinstance(e, ParseCallException)

    try:
        Parser("let foo = (let bar = 1)").parse()
    except Exception as e:
        assert isinstance(e, ParseUnitException)
