MARK = 1
EMPTY = 0


class Halt(Exception):
    pass


class TapeRightInfinite:
    def __init__(self):
        self.pos = 0
        self.tape = [EMPTY]

    def set_cell_to(self, value):
        self.tape[self.pos] = value

    def left(self):
        self.pos -= 1

        if self.pos < 0:
            raise Halt()

    def right(self):
        self.pos += 1

        if len(self.tape) == self.pos:
            self.tape.append(EMPTY)

    def clear(self):
        self.set_cell_to(EMPTY)

    def mark(self):
        self.set_cell_to(MARK)


class Operation:
    def __init__(self, name, op, nextop):
        assert not isinstance(op, Operation)
        assert nextop is None or isinstance(nextop, Operation)
        assert isinstance(name, str)

        self.name = name
        self.op = op
        self.nextop = nextop

    def __repr__(self):
        return f'<Operation {self.name}>'

    def __call__(self):
        self.op()


class ProgramBuilder:
    def __init__(self):
        self.operations = {}
        self.startop = None

    def start(self, operation_name):
        assert self.startop is None

        op = Operation(operation_name, None, None)
        self.startop = op
        self.operations[operation_name] = op
        return op

    def ref(self, operation_name):
        assert self.startop is not None

        op = self.operations.get(operation_name)
        if op is None:
            op = Operation(operation_name, None, None)
            self.operations[operation_name] = op

        return op

    def op(self, operation_name, operation, next_operation_name):
        assert self.startop is not None
        assert operation is not None

        op = self.operations.get(operation_name)
        nextop = self.ref(next_operation_name)
        if op is None:
            op = Operation(operation_name, operation, nextop)
            self.operations[operation_name] = op
        else:
            assert op.op is None
            op.op = operation
            op.nextop = nextop

        return op


class TM:
    def __init__(self, program):
        self.currop = program.startop

    def step(self):
        if self.currop is None or self.currop.op is None:
            raise Halt()

        self.currop.op()
        self.currop = self.currop.nextop
