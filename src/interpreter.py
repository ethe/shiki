# -*- coding: utf-8 -*-
from functools import partial
from .parser import Parser
from .ast_node import *
from .utils import trace
from .utils.tail_call_optimize import trampoline


class Interpreter(object):
    def __init__(self, string):
        self.ast_tree = Parser(string).parse()

    def run(self):
        return self.interpret_expressions(self.ast_tree)

    def interpret_expressions(self, expressions=[], environment=[], context=lambda x: x, inside=False):
        def inner_trace(expression):
            if not inside:
                return trace(expression)
            return expression

        heap = Environment(environment)

        for expression in expressions:
            if isinstance(expression, Return):
                return self.interpret_expression(expression, heap, lambda x: inner_trace(context(x)))
            elif isinstance(expression, Function) or isinstance(expression, Bind):
                trampoline(self.interpret_expression)(
                    expression, heap, lambda x: heap.insert(0, (expression.name, inner_trace(context(x)))))
            else:
                trampoline(self.interpret_expression)(expression, heap, lambda x: inner_trace(context(x)))
        return self.interpret_expression(Nil())

    def interpret_expression(self, expression, environment=[], context=lambda x: x):
        stack = Environment(environment)

        if isinstance(expression, Bind):
            return self.interpret_bind(expression, stack, context)
        elif isinstance(expression, Function):
            return self.interpret_define(expression, stack, context)
        elif isinstance(expression, Call):
            return self.interpret_call(expression, stack, context)
        elif isinstance(expression, Int):
            return self.interpret_int(expression, context)
        elif isinstance(expression, Float):
            return self.interpret_float(expression, context)
        elif isinstance(expression, Return):
            return self.interpret_return(expression, stack, context)
        elif isinstance(expression, Nil):
            return self.interpret_nil(expression, context)
        elif isinstance(expression, Unit):
            return self.interpret_unit(expression, context)

    def interpret_bind(self, bind, environment, context):
        return trampoline(self.interpret_expression)(
            bind.value, environment, lambda x: (bind.name, context(x)))

    def interpret_define(self, function, environment, context):
        environment[function.name] = Closure(function, environment)
        return context((function.name, Closure(function, environment)))

    def interpret_call(self, call, environment, context):

        value = environment[call.name]
        if isinstance(value, Closure):
            function = value.function
            environment = value.environment + environment
            arg_name_index = 0
            for arg in call.args:
                if isinstance(arg, str):
                    arg_value = environment[arg]
                else:
                    arg_value = arg
                environment[function.args[arg_name_index]] = arg_value
                arg_name_index += 1
            return self.interpret_expressions(
                function.expressions, environment, lambda x: context(x), inside=True)
        elif isinstance(value, Call):
            return self.interpret_expression(value, environment, lambda x: context(x))
        else:
            return context(value)

    def interpret_int(self, integer, context):
        return context(integer.value)

    def interpret_float(self, float, context):
        return context(float.value)

    def interpret_return(self, exreturn, environment, context):
        if isinstance(exreturn, Closure):
            return partial(
                self.interpret_expression, exreturn.function.expression, environment, lambda x: context(x))
        else:
            return partial(
                self.interpret_expression, exreturn.expression, environment, lambda x: context(x))

    def interpret_nil(self, nil, context):
        return context(Nil())

    def interpret_unit(self, unit, context):
        return context(unit.call)


class Closure(object):
    def __init__(self, function, environment):
        self.function = function
        self.environment = environment

    def __repr__(self):
        return "<Closure {}>".format(self.function.name)


class Environment(list):
    def __init__(self, environment=[]):
        super(Environment, self).__init__(environment)

    def __add__(self, another):
        environment = super(Environment, self).__add__(another)
        return Environment(environment)

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
