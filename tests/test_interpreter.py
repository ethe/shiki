# -*- coding: utf-8 -*-
from elanus.interpreter import Interpreter


def test_interpret():
    program = """
        let a = 1

        func foo b do
          return b
        end

        let bar = foo a
        let nil_value = nil
    """
    Interpreter(program).run()
