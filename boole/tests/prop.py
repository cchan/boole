# encoding: utf-8

import unittest

from boole.prop import *


class ExpressionTest(unittest.TestCase):
    def test_and(self):
        self.assertEqual(parse('a & b'), And(Variable('a'), Variable('b')))

    def test_double_and(self):
        with self.assertRaises(InvalidExpressionError):
            try:
                parse('a && b')
            except InvalidExpressionError as e:
                print(e.args[0])
                raise

    def test_nesting(self):
        self.assertEqual(parse('a & (b | !(c => (d <=> e)))'),
                         And(Variable('a'),
                             Or(Variable('b'),
                                Not(Implies(Variable('c'),
                                            Iff(Variable('d'),
                                                Variable('e')))))))

    def test_associativity(self):
        self.assertEqual(parse('a & b & c'), And(Variable('a'), And(Variable('b'), Variable('c'))))

    def test_precedence(self):
        self.assertEqual(parse('~a & b | c => d <=> e'),
                         Iff(Implies(Or(And(Not(Variable('a')),
                                            Variable('b')),
                                        Variable('c')),
                                     Variable('d')),
                             Variable('e')))

    def test_unicode(self):
        self.assertEqual(parse(u'¬a ∧ b ∨ c ⇒ d ⇔ e'),
                         Iff(Implies(Or(And(Not(Variable('a')),
                                            Variable('b')),
                                        Variable('c')),
                                     Variable('d')),
                             Variable('e')))

    def test_constant(self):
        self.assertEqual(parse('true & a | false'),
                         Or(And(Constant(True), Variable('a')), Constant(False)))
