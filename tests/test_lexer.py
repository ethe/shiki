# -*- coding: utf-8 -*-
from elanus.lexer import Lexer
from elanus.token import Token
from elanus.scanner import ScanFailedException


def test_lex_int():
    assert Lexer('233').next() == Token("INT")


def test_lex_float():
    assert Lexer('1.02').next() == Token("FLOAT")


def test_lex_newline():
    assert Lexer('\n').next() == Token("NEWLINE")


def test_lex_space():
    assert Lexer('   ').next() == Token("SPACE")


def test_lex_opration():
    for opration in ["+", "-", "*", "/"]:
        assert Lexer(opration).next() == Token("OPRATION")


def test_lex_ident():
    for opration in ["test", "test?", "test!", "test1"]:
        assert Lexer(opration).next() == Token("IDENT")


def test_lex_error():
    try:
        Lexer("???").next()
    except Exception as e:
        assert isinstance(e, ScanFailedException)


def test_lex_function():
    tokens = list(Lexer("func foo x do return x + 1 end"))
    assert tokens == [Token("KEYWORD"), Token("SPACE"), Token("IDENT"),
                      Token("SPACE"), Token("IDENT"), Token("SPACE"),
                      Token("KEYWORD"), Token("SPACE"), Token("KEYWORD"),
                      Token("SPACE"), Token("IDENT"), Token("SPACE"),
                      Token("OPRATION"), Token("SPACE"), Token("INT"),
                      Token("SPACE"), Token("KEYWORD")]


def test_repr():
    assert repr(Lexer("foo").next()) == "<Token IDENT>"


if __name__ == '__main__':
    main()
