from __future__ import print_function

import unittest

from boole.parser.parser import *

class FileParseTest(unittest.TestCase):
    def test_goodfile(self):
        print(parseFile('tests/fixtures/testgood.boole'))
    def test_badfile(self):
        with self.assertRaises(BooleSyntaxError):
            parseFile('tests/fixtures/testbad.boole')
