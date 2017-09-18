"""
boolexpr.py

Processes boolean expressions using a context-free grammar defined in boolexpr.ebnf.
"""

from lark import Lark

with open("boolexpr.ebnf") as bnf:
    BOOLEXPR_MODEL = Lark(bnf.read(), start="boolexpr")

def parse(boolexpr_str):
    """
    Returns a parsed AST based on a given boolean string.
    """
    ast = BOOLEXPR_MODEL.parse(boolexpr_str)
    print(ast.pretty())
    return ast