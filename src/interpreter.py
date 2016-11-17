# -*- coding: utf-8 -*-
from functools import partial
from .parser import Parser
from .ast_node import *
from .utils.tail_call_optimize import trampoline
from .builtin import is_builtin
from .builtin.arithmetic import arithmetic


class Interpreter(object):
    def __init__(self, string):
        self.ast_tree = Parser(string).parse()

    def run(self):
        return self.interpret_expressions(self.ast_tree)

    def interpret_expressions(self, expressions=[], environment=[], inside=False):
        heap = Environment(environment)

        for expression in expressions:
            result = self.trace(trampoline(self.interpret_expression)(expression, heap), inside=inside)
            if isinstance(expression, Return):
                return result
            elif isinstance(expression, Function) or isinstance(expression, Bind):
                heap.insert(0, (expression.name, result))
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
        return trampoline(self.interpret_expression)(bind.value, environment)

    def interpret_define(self, function, environment):
        environment[function.name] = Closure(function, environment)
        return Closure(function, environment)

    def interpret_call(self, call, environment):
        if is_builtin(call):
            call_args = []
            for arg in call.args:
                if isinstance(arg, str):
                    call_args.append(environment[arg])
                else:
                    node = trampoline(self.interpret_expression)(arg, environment)
                    if isinstance(node, Call):
                        node = trampoline(self.interpret_expression)(node, environment)
                    call_args.append(node)
            return arithmetic(call.name, *call_args)

        value = environment[call.name]
        if isinstance(value, Closure):
            function = value.function
            environment = value.environment + environment
            arg_name_index = 0
            for arg in call.args:
                if isinstance(arg, str):
                    arg_value = environment[arg]
                elif isinstance(arg, Unit):
                    arg_value = self.interpret_expression(arg)
                else:
                    arg_value = arg
                environment[function.args[arg_name_index]] = arg_value
                arg_name_index += 1
            return self.interpret_expressions(function.expressions, environment, inside=True)
        elif isinstance(value, Call):
            return partial(self.interpret_expression, value, environment)
        else:
            return value

    def interpret_int(self, integer):
        return integer.value

    def interpret_float(self, float):
        return float.value

    def interpret_return(self, exreturn, environment=[]):
        if isinstance(exreturn, Closure):
            return partial(self.interpret_expression, exreturn.function.expression, environment)
        else:
            return partial(self.interpret_expression, exreturn.expression, environment)

    def interpret_nil(self, nil):
        return Nil()

    def interpret_unit(self, unit):
        return unit.call

    def trace(self, expression, inside):
        if not inside:
            if isinstance(expression, tuple):
                print expression[1]
            else:
                print expression
        return expression


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
