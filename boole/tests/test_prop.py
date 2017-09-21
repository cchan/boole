# encoding: utf-8
from __future__ import print_function, unicode_literals

import unittest

from boole.prop.expr import *


class ExpressionTest(unittest.TestCase):
    def assertInvalid(self, expr):
        with self.assertRaises(InvalidExpressionError):
            try:
                parse(expr)
            except InvalidExpressionError as e:
                print('When checking:', expr)
                print(e.args[0])
                print()
                raise

    def test_and(self):
        self.assertEqual(parse('a & b'), And(Variable('a'), Variable('b')))

    def test_double_and(self):
        self.assertInvalid('a && b')

    def test_nesting(self):
        self.assertEqual(parse('a & (b | !(c => (d <=> e)))'),
                         And(Variable('a'),
                             Or(Variable('b'),
                                Not(Implies(Variable('c'),
                                            Iff(Variable('d'),
                                                Variable('e')))))))

    def test_associativity(self):
        self.assertEqual(parse('a & b & c'), And(Variable('a'), And(Variable('b'), Variable('c'))))

    precedence_result = Iff(Implies(Or(And(Not(Variable('a')),
                                           Variable('b')),
                                       Variable('c')),
                                    Variable('d')),
                            Variable('e'))

    def test_precedence(self):
        self.assertEqual(parse('~a & b | c => d <=> e'),
                         self.precedence_result)

    def test_unicode(self):
        self.assertEqual(parse('¬a ∧ b ∨ c ⇒ d ⇔ e'),
                         self.precedence_result)

    def test_latex(self):
        self.assertEqual(parse(r'¬a \wedge b \vee c \implies d \iff e'),
                         self.precedence_result)

    def test_constant(self):
        self.assertEqual(parse('true & a | false'),
                         Or(And(Constant(True), Variable('a')), Constant(False)))
