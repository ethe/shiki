# -*- coding: utf-8 -*-
from copy import deepcopy
from .parser import Parser
from .ast_node import *


class Interpreter(object):
    def __init__(self, string):
        self.ast_tree = Parser(string).parse()

    def run(self):
        return self.interpret_expressions(self.ast_tree)

    def interpret_expressions(self, expressions=[], environment=[], inside=False):
        heap = Environment(environment)

        for expression in expressions:
            result = self.interpret_expression(expression, heap)
            if result[0] == "return":
                return result[1]
            if not inside:
                print result[1]
            heap.insert(0, result)
        if inside:
            return self.interpret_expression(Nil())

    def interpret_expression(self, expression, environment=[]):
        stack = Environment(environment)

        if isinstance(expression, Bind):
            return self.interpret_bind(expression, stack)
        elif isinstance(expression, Function):
            return self.interpret_define(expression, stack)
        elif isinstance(expression, Call):
            return self.interpret_call(expression, stack)
        elif isinstance(expression, Int):
            return self.interpret_int(expression)
        elif isinstance(expression, Float):
            return self.interpret_float(expression)
        elif isinstance(expression, Return):
            return self.interpret_return(expression, stack)
        elif isinstance(expression, Nil):
            return self.interpret_nil(expression)
        elif isinstance(expression, Unit):
            return self.interpret_unit(expression)

    def interpret_bind(self, bind, environment):
        return (bind.name, self.interpret_expression(bind.value, environment)[1])

    def interpret_define(self, function, environment):
        return (function.name, Closure(function, environment))

    def interpret_call(self, call, environment):
        value = environment[call.name]
        if isinstance(value, Closure):
            function = value.function
            environment = value.environment
            arg_name_index = 0
            for arg in call.args:
                arg_value = environment[arg] if isinstance(arg, str) else self.interpret_expression(arg, environment)[1]
                environment[function.args[arg_name_index]] = arg_value
                arg_name_index += 1
            return self.interpret_expressions(function.expressions, environment, inside=True)
        elif isinstance(value, Call):
            return self.interpret_expression(value, environment)
        else:
            return ('', value)

    def interpret_int(self, integer):
        return ('', integer.value)

    def interpret_float(self, float):
        return ('', float.value)

    def interpret_return(self, exreturn, environment=[]):
        if isinstance(exreturn, Closure):
            return ("return", self.interpret_expression(exreturn.function.expression, environment))
        else:
            return ("return", self.interpret_expression(exreturn.expression, environment))

    def interpret_nil(self, nil):
        return ('', Nil())

    def interpret_unit(self, unit):
        return ('', unit.call)


class Closure(object):
    def __init__(self, function, environment):
        self.function = function
        self.environment = environment

    def __repr__(self):
        return "<Closure {}>".format(self.function.name)


class Environment(list):
    def __init__(self, evironment=[]):
        super(Environment, self).__init__(evironment)

    def __getitem__(self, key):
        for pair in self.__iter__():
            if key == pair[0]:
                return pair[1]
        raise RuntimeNameError(key)

    def __setitem__(self, key, value):
        self.insert(0, (key, value))
        return self


class RuntimeNameError(Exception):
    def __init__(self, name):
        super(RuntimeNameError, self).__init__("Name {name} is not defined.".format(name=name))
