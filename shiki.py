#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src.interpreter import Interpreter


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            Interpreter(f.read()).run()


if __name__ == '__main__':
    main()
