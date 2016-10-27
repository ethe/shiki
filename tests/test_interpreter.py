# -*- coding: utf-8 -*-
from elanus.interpreter import Interpreter


def test_interpret():
    program = """
        let a = 1
        func foo do
          return a
        end
        let bar = foo
    """
    Interpreter(program).run()
