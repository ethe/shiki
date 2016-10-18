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
                raise ScanFailedException()

    def __iter__(self):
        return self.stream.__iter__()


class ScanFailedException(Exception):
    def __init__(self):
        super(ScanFailedException, self).__init__("Can not scan anymore.")
