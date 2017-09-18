"""
boole.py
"""

import boolexpr
import re

# boolexpr.parse("a | b & c => d | b <=> asdf")

# Each state:
# state number [int]:
#   array of
#     (condition [regex], doing [callback that gets match()], transition_to [int])

EOF = "###EOF###"


def state(expecting=None):
    def func_modifier(currstate):
        def modified_func(filename, linenum, orig_line):
            line = orig_line.strip()
            if line.startswith("%") or len(line) == 0:
                return globals()[currstate.__name__]
            try:
                transition_to = currstate(line)
            except SyntaxError as e:
                raise SyntaxError("Error raised in state " + currstate.__name__ + ": " + repr(e),
                                  (filename, linenum, 0, orig_line))
            if transition_to is None:
                if expecting is not None:
                    raise SyntaxError("Expected " + expecting, (filename, linenum, 0, orig_line))
                else:
                    raise SyntaxError("Unexpected line", (filename, linenum, 0, orig_line))
            else:
                return transition_to

        modified_func.__name__ = currstate.__name__
        return modified_func

    return func_modifier


@state(expecting="#u declaration")
def initial(line):
    if line.startswith("#u "):
        D["users"] = line[3:].split(' ')
        return user_declared


@state(expecting="#a declaration")
def user_declared(line):
    if line.startswith("#a "):
        D["assignment"] = line[3:]
        return header_declared


@state(expecting="#q declaration")
def header_declared(line):
    if line.startswith("#q "):
        D["currentQuestion"] = line[3:]
        if not D["currentQuestion"].startswith(D["assignment"]):
            raise SyntaxError("Question number does not start with assignment number.")
        else:
            return question_declared
    print("reached end")


@state(expecting="#check declaration")
def question_declared(line):
    if line == EOF:
        return True
    if line.startswith("#check "):
        check = line[7:]
        if check == "NONE":
            return check_NONE
        else:
            raise SyntaxError("The #check \"" + check + "\" is invalid")


@state(expecting="solution lines")
def check_NONE(line):
    if line.startswith("#q "):
        pass
    elif line.startswith("#a "):
        pass
    elif line == EOF:
        return True
    else:  # it's a line of solution!
        print("Line of solution in check_NONE!", line)
        return check_NONE


state = initial
D = {}


def parse(file):
    global state
    for i, orig_line in enumerate(file):
        print("Current state:", state.__name__, "\nNew line of code:", orig_line)
        state = state(filename, i + 1, orig_line)
    state = state(filename, i + 2, EOF)
    if state is True:
        print("Successfully exited.")


if __name__ == "__main__":
    filename = "testgood.boole"  # input("Filename: ")
    with open(filename) as file:
        parse(file)
