# -*- coding: utf-8 -*-
from src.ast_node import BuiltinFunction, TrueType, FalseType


class And(BuiltinFunction):
    def __init__(self):
        super(And, self).__init__(name="and", args=["one", "another"])

    def oprate(self):
        result = self.values[0] and self.values[1]
        if result:
            return TrueType(result)
        return FalseType(result)


builtin = [And()]
