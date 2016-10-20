# -*- coding: utf-8 -*-
from elanus.parser import Parser, ParseException
from elanus.ast_node import *


def test_bind():
    def test(node, name, value):
        node = Parser(node).parse()
        assert node.expressions[0].name == name
        assert node.expressions[0].value == value

    test("\nlet foo = 1", "foo", Int("1"))
    test("let foo = 1.1", "foo", Float("1.1"))

    test("let foo = bar a 1", "foo", Call("bar", ["a", Int("1")]))


def test_error():
    try:
        Parser("let foo = =").parse()
    except Exception as e:
        assert isinstance(e, ParseException)
