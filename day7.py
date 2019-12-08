from itertools import chain, permutations
from collections import deque

code = [3,8,1001,8,10,8,105,1,0,0,21,38,55,68,93,118,199,280,361,442,99999,3,9,1002,9,2,9,101,5,9,9,102,4,9,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,1001,9,4,9,4,9,99,3,9,101,4,9,9,102,3,9,9,4,9,99,3,9,102,2,9,9,101,4,9,9,102,2,9,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,1002,9,2,9,1001,9,2,9,1002,9,5,9,1001,9,2,9,1002,9,4,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]

FIFO = deque()


def get_op_and_arg_modes(opcode):
    opcode = str(opcode)
    
    if len(opcode) < 2:
        opcode = '0' + opcode

    op = opcode[-2:]
    arg_modes = opcode[:-2]

    num_args = idx_inc[op] - 1

    nof_missing_zeros = num_args - len(arg_modes)

    arg_modes = ''.zfill(nof_missing_zeros) + arg_modes
    arg_modes = [int(each_char) for each_char in arg_modes[::-1]]
    return op, arg_modes 


# pattern: arg1, mode1, arg2, mode2, ... argn, moden, ram 
def mul_(arg1, arg1_mode, 
         arg2, arg2_mode, 
         res_arg, res_arg_mode, ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]
    ram[res_arg] = arg1 * arg2
    return ram, idx


def add_(arg1, arg1_mode, 
         arg2, arg2_mode, 
         res_arg, res_arg_mode, ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]
    ram[res_arg] = arg1 + arg2
    return ram, idx


def output_(arg1, arg1_mode, ram, idx):
    global FIFO
    value = (1-arg1_mode)*ram[arg1] + arg1_mode*arg1
    #print(value)
    FIFO.appendleft(value)
    return ram, idx


def input_(arg1, arg1_mode, ram, idx):
    # arg1_mode is bound to be 0
    global FIFO
    # val = input('insert value \n')
    val = FIFO.pop()
    ram[arg1] = int(val)
    return ram, idx

def jump_if_true(arg1, arg1_mode, arg2, arg2_mode, ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]

    if arg1 != 0:
        idx = arg2
    return ram, idx


def jump_if_false(arg1, arg1_mode, arg2, arg2_mode, ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]

    if arg1 == 0:
        idx = arg2
    return ram, idx


def less_than(arg1, arg1_mode, arg2, arg2_mode, arg3, arg3_mode, 
              ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]

    if arg1 < arg2:
        ram[arg3] = 1
    else:
        ram[arg3] = 0

    return ram, idx

def equals_(arg1, arg1_mode, arg2, arg2_mode, arg3, arg3_mode, 
              ram, idx):
    if arg1_mode == 0:
        arg1 = ram[arg1]
    if arg2_mode == 0:
        arg2 = ram[arg2]

    if arg1 == arg2:
        ram[arg3] = 1
    else:
        ram[arg3] = 0

    return ram, idx

dispatch = {
        '01': add_, 
        '02': mul_,
        '03': input_,
        '04': output_,
        '05': jump_if_true,
        '06': jump_if_false,
        '07': less_than,
        '08': equals_
}


# program counter increment by instruction
idx_inc = {
    '01': 4,  # add
    '02': 4,  # mul
    '03': 2,  # input
    '04': 2,  # output
    '05': 3,  # jump if true
    '06': 3,  # jump if false
    '07': 4,  # less than
    '08': 4,  # equals
    '99': 1
}


def run_prog(code):

    idx = 0
    while idx < len(code):
        op, args_mode = get_op_and_arg_modes(code[idx])
        if op != '99':
            args_ = code[idx + 1: idx + idx_inc[op]]
        else:
            break
        args_and_modes = list(chain.from_iterable(zip(args_, args_mode)))
        code, new_idx = dispatch[op](*args_and_modes, code, idx)
        if new_idx == idx:
            idx += idx_inc[op]
        else:
            idx = new_idx


def calc_amps_output(code, phases):
    global FIFO
    FIFO = deque()
    for idx, phase in enumerate(phases):
        print(phase)
        if idx == 0:
            FIFO.appendleft(phase)
            FIFO.appendleft(0)
        else:
            FIFO.append(phase)
        run_prog(code)
    return FIFO.pop()


if __name__ == "__main__":
    assert(('01', [1, 0, 0]) == get_op_and_arg_modes(101))
    assert(('02', [0, 1, 0]) == get_op_and_arg_modes(1002))
    assert(('03', [0]) == get_op_and_arg_modes(3))
    assert(('04', [0]) == get_op_and_arg_modes(4))

    code_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phases_1 = ['4', '3', '2', '1', '0']
    assert(calc_amps_output(code_1, phases_1) == 43210)

    code_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    phases_2 = [0, 1, 2, 3, 4]
    assert(calc_amps_output(code_2, phases_2) == 54321)

    code_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phases_3 = [1,0,4,3,2]
    assert(calc_amps_output(code_3, phases_3) == 65210)

            
    max_output = 0
    for each_phases in permutations([0, 1, 2, 3, 4]):
        amp_out = calc_amps_output(code, each_phases)
        if amp_out > max_output:
            max_output = amp_out

    print(max_output)

