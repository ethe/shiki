# -*- coding: utf-8 -*-
from elanus.parser import Parser


def test_bind():
    node = Parser("let foo = 1").parse()
    assert node.expressions[0].name == 'foo'
    assert node.expressions[0].value.value == '1'
