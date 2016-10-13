# -*- coding: utf-8 -*-
import pytest
from elanus.lexer import Lexer
from elanus.token import *


def test_lex_int():
    assert Lexer('233').result[0].type == "INT"


def test_lex_float():
    assert Lexer('1.02').result[0].type == "FLOAT"


def test_lex_newline():
    assert Lexer('\n').result[0].type == "NEWLINE"


def test_lex_space():
    assert Lexer('   ').result[0].type == "SPACE"


def test_lex_opration():
    for opration in ["+", "-", "*", "/"]:
        assert Lexer(opration).result[0].type == "OPRATION"


def test_lex_ident():
    for opration in ["test", "test?", "test!", "test1"]:
        assert Lexer(opration).result[0].type == "IDENT"


def test_lex_error():
    assert Lexer("???").result == []


if __name__ == '__main__':
    main()
