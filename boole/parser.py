from __future__ import print_function

from functools import wraps

import prop
import deduct

class BooleSyntaxError(SyntaxError):
    pass


def state(expecting=None, check=None):
    def func_modifier(state):
        @wraps(state)
        def modified_func(self, filename, linenum, orig_line):
            line = orig_line.strip()
            if line.startswith('%') or len(line) == 0:
                return getattr(self, state.__name__)
            if check is not None:
                if line.startswith('#q '):
                    return self.header_declared(filename, linenum, orig_line)
                elif line.startswith('#check '):
                    return self.question_declared(filename, linenum, orig_line)
                elif line == self.EOF:
                    return True
                else: # It's a line of solution!
                    pass
            try:
                transition_to = state(self, line)
                if check is not None:
                    return getattr(self, state.__name__)
            except BooleSyntaxError as e:
                raise BooleSyntaxError('Error raised in state ' + state.__name__ + ': ' + repr(e),
                                       (filename, linenum, 0, orig_line))
            if transition_to is None:
                if expecting is not None:
                    raise BooleSyntaxError('Expected ' + expecting, (filename, linenum, 0, orig_line))
                else:
                    raise BooleSyntaxError('Unexpected line', (filename, linenum, 0, orig_line))
            else:
                return transition_to
        return modified_func
    return func_modifier

class FileParser(object):
    def __init__(self, file):
        self.state = self.initial
        self.D = {}
        self.EOF = '###EOF###'
        self.users = None
        self.assignment = None

        for i, orig_line in enumerate(file):
            print('Current state:', self.state.__name__)
            print('New line of code:', orig_line)
            self.state = self.state(filename, i + 1, orig_line)
        self.state = self.state(filename, i + 2, self.EOF)
        if self.state is True:
            print('Successfully exited.')

    @state(expecting='#u declaration')
    def initial(self, line):
        if line.startswith('#u '):
            self.users = line[3:].split(' ')
            return self.user_declared

    @state(expecting='#a declaration')
    def user_declared(self, line):
        if line.startswith('#a '):
            self.assignment = line[3:]
            return self.header_declared

    @state(expecting='#q declaration')
    def header_declared(self, line):
        if line.startswith('#q '):
            self.currentQuestion = line[3:]
            return self.question_declared

    @state(expecting='#check declaration')
    def question_declared(self, line):
        if line == self.EOF:
            return True
        if line.startswith('#check '):
            check = line[7:]
            nextstate = getattr(self, "check_" + check, None)
            if nextstate is None:
                raise BooleSyntaxError('The #check "%s" is invalid' % check)
            else:
                return nextstate

    @state(expecting='solution lines for NONE', check='NONE')
    def check_NONE(self, line):
        print('Line of solution in check_NONE!', line)

    @state(expecting='solution lines for PROP', check='PROP')
    def check_PROP(self, line):
        try:
            print('Line of solution in check_PROP!')
            print(prop.expr.parse(line))
        except prop.expr.InvalidExpressionError as e:
            raise BooleSyntaxError(*e.args)

    @state(expecting='solution lines for PRED')
    def check_PRED(self, line):
        raise NotImplementedError

    @state(expecting='solution lines for TP')
    def check_TP(self, line):
        raise NotImplementedError

    @state(expecting='solution lines for ND')
    def check_ND(self, line):
        raise NotImplementedError

    @state(expecting='solution lines for ST')
    def check_ST(self, line):
        raise NotImplementedError

    @state(expecting='solution lines for Z')
    def check_Z(self, line):
        raise NotImplementedError

    @state(expecting='solution lines for PC')
    def check_PC(self, line):
        raise NotImplementedError

if __name__ == '__main__':
    filename = 'tests/testgood.boole'  # input('Filename: ')
    with open(filename) as file:
        parsed = FileParser(file)
