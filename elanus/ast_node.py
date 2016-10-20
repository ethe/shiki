# -*- coding: utf-8 -*-
class Node(object):
    def __init__(self, line=0):
        self.line = line


class Expressions(Node):
    def __init__(self, expressions, line=0):
        super(Expressions, self).__init__(line)
        self.expressions = expressions

    def __eq__(self, another):
        if not isinstance(another, Call):
            return False
        return self.expressions == another.expressions


class Expression(Node):
    def __repr__(self):
        return "<{} {}>".format(self.__class__, self.value if hasattr(self, "value") else self.__hash__())


class Call(Expression):
    def __init__(self, name="", args=[], line=0):
        super(Call, self).__init__(line)
        self.name = name
        self.args = args

    def __eq__(self, another):
        if not isinstance(another, Call):
            return False
        return self.name == another.name and self.args == another.args


class Bind(Expression):
    def __init__(self, name, value, line=0):
        super(Expression, self).__init__(line)
        self.name = name
        self.value = value

    def __eq__(self, another):
        if not isinstance(another, Bind):
            return False
        return self.name == another.name and self.value == another.value


class Unit(Expression):
    def __init__(self, call, line=0):
        super(Expression, self).__init__(line)
        self.call = call

    def __eq__(self, another):
        if not isinstance(another, Unit):
            return False
        return self.call == another.call


class Number(Expression):
    def __init__(self, number, line=0):
        super(Number, self).__init__(line)
        self.value = number

    def __eq__(self, another):
        if not isinstance(another, Number):
            return False
        return self.value == another.value


class Int(Number):
    pass


class Float(Number):
    pass
