from functools import wraps


class BooleSyntaxError(SyntaxError):
    pass


def state(expecting=None):
    def func_modifier(state):
        @wraps(state)
        def modified_func(self, filename, linenum, orig_line):
            line = orig_line.strip()
            if line.startswith('%') or len(line) == 0:
                return getattr(self, state.__name__)
            try:
                transition_to = state(self, line)
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
            if not self.currentQuestion.startswith(self.assignment):
                raise BooleSyntaxError('Question number does not start with assignment number.')
            else:
                return self.question_declared
        print('reached end')

    @state(expecting='#check declaration')
    def question_declared(self, line):
        if line == self.EOF:
            return True
        if line.startswith('#check '):
            check = line[7:]
            if check == 'NONE':
                return self.check_NONE
            else:
                raise BooleSyntaxError('The #check "%s" is invalid' % check)

    @state(expecting='solution lines')
    def check_NONE(self, line):
        if line.startswith('#q '):
            pass
        elif line.startswith('#a '):
            pass
        elif line == self.EOF:
            return True
        else:  # it's a line of solution!
            print('Line of solution in check_NONE!', line)
            return self.check_NONE


if __name__ == '__main__':
    filename = 'tests/testgood.boole'  # input('Filename: ')
    with open(filename) as file:
        parsed = FileParser(file)
