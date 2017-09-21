# coding: utf-8
from __future__ import unicode_literals

from lark import Lark

from boole.prop.expr import prop_symbols, prop_expr, PropExpressionTransform, Expression

proof_symbols = '''
PROVES: "|-" | "⊢"
PROOF_LINE_NUMBER_END: ")"
SUBPROOF_OPEN: "{"
SUBPROOF_CLOSE: "}"

PREMISE: "premise"
BY: "by"
RULES: "and_i"
     | "and_e"
     | "or_i"
     | "or_e"
     | "lem"
     | "imp_e"
     | "not_e"
     | "not_not_i"
     | "not_not_e"
     | "iff_i"
     | "iff_e"
     | "trans"
     | "iff_mp"
     | "exists_i"
     | "forall_e"
     | "true"
     | "eq_i"
     | "eq_e"
ON: "on"
COMMA: ","
RANGE_TO: "-"
'''

proof_syntax = '''
%import common.INT
%import common.NEWLINE

proof_premise: propexpr (COMMA propexpr)*                           -> on_proof_premise
proof_decl: proof_premise PROVES propexpr                           -> on_proof_decl

line_list: INT (COMMA INT)* | INT RANGE_TO INT 
?reasoning: PREMISE                                                 -> on_reason_premise
          | BY RULES ON line_list                                   -> on_reason_rule

subproof: SUBPROOF_OPEN proof_lines SUBPROOF_CLOSE                  -> on_subproof
proof_line: INT PROOF_LINE_NUMBER_END propexpr reasoning subproof?  -> on_proof_line

proof_lines: proof_line (NEWLINE+ proof_line)* NEWLINE*
proof: proof_decl NEWLINE+ proof_lines
'''


class Reasoning(object):
    pass


class ReasonPremise(object):
    def __repr__(self):
        return 'ReasonPremise()'

    def __eq__(self, other):
        return isinstance(other, ReasonPremise)


class ProofLine(object):
    def __init__(self, number, expr, reason, children=None):
        self.number = number
        self.expr = expr
        self.reason = reason
        self.children = children

    def __repr__(self):
        return 'ProofLine(%d, %r, %r, %r)' % (self.number, self.expr, self.reason, self.children)

    def __eq__(self, other):
        return (self.number == other.number and
                self.expr == other.expr and
                self.reason == other.reason and
                self.children == other.children)


class DeductProofTransform(PropExpressionTransform):
    def on_proof_premise(self, *args):
        return [expr for expr in args if isinstance(expr, Expression)]

    def on_proof_decl(self, premise, proves, conclusion):
        return premise, conclusion

    def on_proof_line(self, number, open_end, expr, reason, subproofs=None):
        return ProofLine(int(number.value), expr, reason, subproofs)

    def on_reason_premise(self, *args):
        return ReasonPremise()
