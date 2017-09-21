from __future__ import print_function

import unittest
from functools import partial

from boole.deduct.proof import *
from boole.prop.expr import *

parser_of_symbol = partial(Lark, prop_symbols + prop_expr + proof_symbols + proof_syntax)
transform = DeductProofTransform().transform


class ProofTest(unittest.TestCase):
    def test_parse_proof_decl(self):
        self.assertEqual(transform(parser_of_symbol(start='proof_decl').parse('a & b, c |- a')),
                         ([And(Variable('a'), Variable('b')), Variable('c')], Variable('a')))

    def test_parse_proof_line(self):
        self.assertEqual(transform(parser_of_symbol(start='proof_line').parse('1) a & b premise')),
                         ProofLine(1, And(Variable('a'), Variable('b')), ReasonPremise()))
