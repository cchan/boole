from __future__ import print_function

import unittest

from boole.parser.parser import *

import os

class FileParseTest(unittest.TestCase):
    def parseFileRelative(self, filename):
        dir = os.path.dirname(__file__)
        return parseFile(os.path.join(dir, filename))

    def test_goodfile(self):
        print(self.parseFileRelative('fixtures/testgood.boole'))

    def test_badfile(self):
        with self.assertRaises(BooleSyntaxError):
            self.parseFileRelative('fixtures/testbad.boole')
