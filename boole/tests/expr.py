import unittest

from boole.expr import *


class ExpressionTest(unittest.TestCase):
    def test_and(self):
        self.assertEqual(parse('a & b'), And(Variable('a'), Variable('b')))

    def test_double_and(self):
        with self.assertRaises(InvalidExpressionError):
            parse('a && b')
