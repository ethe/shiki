# -*- coding: utf-8 -*-
import re


class StringScanner(object):
    def __init__(self, string):
        self.string = string
        self.lexicon = [(name, re.compile(phrase)) for name, phrase in self.lexicon()]

    def scan(self):
        while self.string != '':
            success = False
            for name, phrase in self.lexicon:
                match = phrase.match(self.string)
                if match:
                    self.string = self.string[match.end():]
                    success = True
                    yield getattr(self, name)(match.group())
            if not success:
                raise ScanFailedException()


class ScanFailedException(Exception):
    def __init__(self):
        super(ScanFailedException, self).__init__("Can not scan anymore.")
