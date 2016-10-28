# -*- coding: utf-8 -*-
from elanus.interpreter import Interpreter


def test_interpret():
    program = """
        let a = 1

        func foo do
          let a = 1.1
          return a
        end

        func bar n do
          return n
        end

        let bar = bar foo
        a
        let nil_value = nil

        func bar n do
          return n
        end

        func foo n do
          return n
        end

        let a = foo (bar 1)
    """
    Interpreter(program).run()
