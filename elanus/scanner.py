# -*- coding: utf-8 -*-
import re


class StringScanner(object):
    def __init__(self, string):
        self.string = string
        self.word = None
        self.lexicon = [(name, re.compile(phrase)) for name, phrase in self.lexicon()]
        self.stream = self.scan()
        self.next = self.stream.next

    def scan(self):
        while self.string != '':
            success = False
            for name, phrase in self.lexicon:
                match = phrase.match(self.string)
                if match:
                    self.string = self.string[match.end():]
                    success = True
                    self.word = getattr(self, name)(match.group())
                    yield self.word
            if not success:
                raise ScanException(self.line, self.column)

    def eof(self):
        return self.string == ""

    def __iter__(self):
        return self.stream.__iter__()


class ScanException(Exception):
    def __init__(self, line, column):
        super(ScanException, self).__init__(
            "Can not itdentify word, at line {line}, column {column}".format(line=line, column=column))
