# -*- coding: utf-8 -*-
from src.ast_node import BuiltinFunction, Number


class Add(BuiltinFunction):
    def __init__(self):
        super(Add, self).__init__(name="+", args=["one", "another"])

    def oprate(self):
        return Number(self.values[0] + self.values[1])


class Minus(BuiltinFunction):
    def __init__(self):
        super(Minus, self).__init__(name="-", args=["one", "another"])

    def oprate(self):
        return Number(self.values[0] - self.values[1])


class Multiply(BuiltinFunction):
    def __init__(self):
        super(Multiply, self).__init__(name="*", args=["one", "another"])

    def oprate(self):
        return Number(self.values[0] * self.values[1])


class Division(BuiltinFunction):
    def __init__(self):
        super(Division, self).__init__(name="/", args=["one", "another"])

    def oprate(self):
        return Number(self.values[0] / self.values[1])


builtin = [Add(), Minus(), Multiply(), Division()]
