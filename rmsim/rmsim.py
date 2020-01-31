#!/usr/bin/python
import sys

program = [[]]
registers = []
labels = {}


def execute(lineNo):
    global program
    # Halt execution if the label is 'HALT'
    if lineNo == -1:
        print('registers ' + ' '.join(map(str, registers)))
        sys.exit(0)
    # Else, execute and move onto next line
    else:
        line = program[lineNo]
        # If a labelled line, remove label before execution
        if line[0][:-1] in labels:
            line = line[1:]

        # Execution of instructions
        if line[0] == 'decjz':
            decjz(line[1], line[2])
        elif line[0] == 'inc':
            inc(line[1])

        return execute(lineNo + 1)


def inc(register):
    global registers
    # Retrieve register index
    regIndex = int(register.split('r')[1])
    # If register has not been created yet, initialise it to zero (along with any intermediate registers)
    while regIndex > len(registers) - 1:
        registers.append(0)
    # Increment register value
    registers[regIndex] += 1
    return


def decjz(register, label):
    global registers
    # Retrieve register index
    regIndex = int(register.split('r')[1])
    # If register has not been created yet, initialise it to zero (along with any intermediate registers)
    while regIndex > len(registers) - 1:
        registers.append(0)
    # DECJZ behaviour
    if registers[regIndex] == 0:
        if label == 'HALT':
            execute(-1)
        else:
            lineNo = labels.get(label)
            execute(lineNo)
    else:
        registers[regIndex] -= 1
        return


def parseLines():
    global program
    global registers
    # Retrieve initial register values
    registers.append(map(int, program[0][1:len(program[0])]))
    registers = registers[0]
    # Remove registers line from program
    program = program[1:]

    # Retrieve labels and add them to dict
    for i in range(len(program)):
        if program[i][0][-1] == ':':
            labels[program[i][0][:-1]] = i


def main():
    global program
    while program[-1] != ['end']:
        line = sys.stdin.readline()
        program.append(line.split())

    program = program[1:len(program)-1]
    parseLines()

    # Begin program execution
    execute(0)


if __name__ == '__main__':
    main()
