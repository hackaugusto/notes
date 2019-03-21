from m import ProgramBuilder, TapeRightInfinite, TM

builder = ProgramBuilder()
tape = TapeRightInfinite()

builder.start('a')
builder.op('a', tape.right, 'b')
builder.op('b', tape.mark, 'c')
builder.op('c', tape.right, 'a')

machine = TM(builder)

for _ in range(10):
    machine.step()
    print(tape.tape)
