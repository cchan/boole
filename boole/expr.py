"""
boolexpr.py

Processes boolean expressions using a context-free grammar defined in expr.ebnf
and transform it into an AST.
"""

import os

from lark import Lark, InlineTransformer, ParseError

with open(os.path.join(os.path.dirname(__file__), 'expr.ebnf')) as bnf:
    parser = Lark(bnf.read(), start='boolexpr')


__all__ = ['Expression', 'InvalidExpressionError', 'Variable', 'And', 'Or', 'Implies', 'Iff', 'Not', 'parse']


class Expression(object):
    pass


class InvalidExpressionError(ValueError):
    pass


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Variable(%r)' % self.name

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name


class Operation(Expression):
    name = None


class UnaryOperation(Operation):
    def __init__(self, operand):
        self.operand = operand

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.operand == other.operand


class BinaryOperation(Operation):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.left == other.left and self.right == other.right


class And(BinaryOperation):
    name = 'AND'


class Or(BinaryOperation):
    name = 'OR'


class Not(UnaryOperation):
    name = 'NOT'


class Implies(BinaryOperation):
    name = 'IMP'


class Iff(BinaryOperation):
    name = 'IFF'


def unary_transform(operator):
    def wrapper(self, prefix, operand):
        return operator(operand)
    return wrapper


def binary_transform(operator):
    def wrapper(self, operand1, infix, operand2):
        return operator(operand1, operand2)
    return wrapper


class BooleanExpressionTransform(InlineTransformer):
    on_iff = binary_transform(Iff)
    on_imp = binary_transform(Implies)
    on_and = binary_transform(And)
    on_or = binary_transform(Or)
    on_not = unary_transform(Not)

    def on_literal(self, literal):
        return Variable(literal.value)

    def on_result(self, result):
        return result

    def on_paren(self, lparen, expr, rparen):
        return expr


def parse(boolexpr_str):
    """
    Returns a parsed AST based on a given boolean string.
    """
    try:
        ast = parser.parse(boolexpr_str)
    except ParseError as e:
        raise InvalidExpressionError(*e.args)
    return BooleanExpressionTransform().transform(ast)