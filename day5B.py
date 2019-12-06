from itertools import chain

code = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,91,67,225,1102,67,36,225,1102,21,90,225,2,13,48,224,101,-819,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,62,9,225,1,139,22,224,101,-166,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,102,41,195,224,101,-2870,224,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,1101,46,60,224,101,-106,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1001,191,32,224,101,-87,224,224,4,224,102,8,223,223,1001,224,1,224,1,223,224,223,1101,76,90,225,1101,15,58,225,1102,45,42,224,101,-1890,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,101,62,143,224,101,-77,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,55,54,225,1102,70,58,225,1002,17,80,224,101,-5360,224,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,344,101,1,223,223,107,677,226,224,1002,223,2,223,1006,224,359,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1008,226,677,224,102,2,223,223,1006,224,434,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,449,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,494,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,509,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,1107,677,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,7,677,226,224,1002,223,2,223,1006,224,584,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,614,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,659,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226]




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


# pattern: arg1, mode1, arg2, mode2, ... argn, moden, ram, idx
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
    value = (1-arg1_mode)*ram[arg1] + arg1_mode*arg1
    print(value)
    return ram, idx


def input_(arg1, arg1_mode, ram, idx):
    # arg1_mode is bound to be 0
    val = input('insert value \n')
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


if __name__ == "__main__":
    assert(('01', [1, 0, 0]) == get_op_and_arg_modes(101))
    assert(('02', [0, 1, 0]) == get_op_and_arg_modes(1002))
    assert(('03', [0]) == get_op_and_arg_modes(3))
    assert(('04', [0]) == get_op_and_arg_modes(4))
    idx = 0
    test_code = [1002, 4, 3, 4, 33]
    op, args_mode = get_op_and_arg_modes(test_code[idx])
    if op != '99':
        args_ = test_code[idx + 1:idx + idx_inc[op]]
    assert args_ == [4, 3, 4]
    args_and_modes = list(chain.from_iterable(zip(args_, args_mode)))
    assert (dispatch[op](*args_and_modes, [1, 2, 3, 4, 33], 0) == [1, 2, 3, 4, 99], 0)
    idx += idx_inc[op]
    assert idx == 4
    
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

        print('idx = {}'.format(idx))
