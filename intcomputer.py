from itertools import chain, permutations, cycle
from collections import deque

class RAM(list):

    def __init__(self, *args):
        return super(RAM, self).__init__(*args)

    def _expand_if_needed(self, addr):
        #if isinstance(addr, slice):
        #    start, stop, step = addr.indices(len(self))
        if isinstance(addr, int) and addr < 0:
            raise KeyError('trying to address {}'.format(addr))
        if isinstance(addr, int) and addr >= len(self):
            self.extend([0 for _ in range(addr)])

    def __getitem__(self, addr, *args):
        self._expand_if_needed(addr)
        return super(RAM, self).__getitem__(addr, *args) 

    def __setitem__(self, addr, *args):
        self._expand_if_needed(addr)
        return super(RAM, self).__setitem__(addr, *args)

class IntcodeComputer:

    def __init__(self, in_que, out_que, id_=None, code=None):
        self.in_que = in_que
        self.out_que = out_que
        self.idx = 0
        self.op = ''
        self.id_ = id_
        self.last_input = None
        self.wait_for_input = False
        self.relative_base = 0
        if code is not None:
            self.code = RAM(code)
        else:
            self.code = None
        self.dispatch = {
                '01': self.add_, 
                '02': self.mul_,
                '03': self.input_,
                '04': self.output_,
                '05': self.jump_if_true,
                '06': self.jump_if_false,
                '07': self.less_than,
                '08': self.equals_,
                '09': self.set_relative_base
        }
        
        # program counter increment by instruction
        self.idx_inc = {
            '01': 4,  # add
            '02': 4,  # mul
            '03': 2,  # input
            '04': 2,  # output
            '05': 3,  # jump if true
            '06': 3,  # jump if false
            '07': 4,  # less than
            '08': 4,  # equals
            '09': 2,  # set relative base
            '99': 1
        }

    def set_relative_base(self, val, val_mode, ram, idx):
        val = self._arg_eval(val, val_mode, ram)
        self.relative_base += val
        return ram, idx

    def _arg_eval(self, arg_, arg_mode, ram):
        if arg_mode == 0:
            return ram[arg_]
        elif arg_mode == 1:
            return arg_
        elif arg_mode == 2:
            return ram[arg_ + self.relative_base]

    def _arg_write(self, arg_, arg_mode, value, ram):
        if arg_mode == 0:
            ram[arg_] = value
        elif arg_mode == 1:
            ram[ram[arg_]] = value
        elif arg_mode == 2:
            ram[arg_+self.relative_base] = value
        return ram

    def get_op_and_arg_modes(self, opcode):
        opcode = str(opcode)
        
        if len(opcode) == 1:
            opcode = '0' + opcode
    
        self.op = opcode[-2:]
        arg_modes = opcode[:-2]
        
        num_args = self.idx_inc[self.op] - 1
    
        nof_missing_zeros = num_args - len(arg_modes)
    
        arg_modes = ''.zfill(nof_missing_zeros) + arg_modes
        arg_modes = [int(each_char) for each_char in arg_modes[::-1]]
        return self.op, arg_modes 
    
    # pattern: arg1, mode1, arg2, mode2, ... argn, moden, ram 
    def mul_(self,
             arg1, arg1_mode, 
             arg2, arg2_mode, 
             res_arg, res_arg_mode, ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)

        ram = self._arg_write(res_arg, res_arg_mode, arg1 * arg2, ram)
        return ram, idx
    
    def add_(self,
             arg1, arg1_mode, 
             arg2, arg2_mode, 
             res_arg, res_arg_mode, ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)
        ram = self._arg_write(res_arg, res_arg_mode, arg1 + arg2, ram)
        return ram, idx
    
    
    def output_(self, arg1, arg1_mode, ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        self.out_que.appendleft(arg1)
        return ram, idx
    
    def input_(self, arg1, arg1_mode, ram, idx):
        val = self.in_que.pop()
        ram = self._arg_write(arg1, arg1_mode, val, ram)
        return ram, idx
    
    def jump_if_true(self, arg1, arg1_mode, arg2, arg2_mode, ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)
    
        if arg1 != 0:
            idx = arg2
        return ram, idx
    
    
    def jump_if_false(self, arg1, arg1_mode, arg2, arg2_mode, ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)
    
        if arg1 == 0:
            idx = arg2
        return ram, idx
    
    
    def less_than(self, arg1, arg1_mode, arg2, arg2_mode, arg3, arg3_mode, 
                  ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)
    
        if arg1 < arg2:
            ram = self._arg_write(arg3, arg3_mode, 1, ram)
        else:
            ram = self._arg_write(arg3, arg3_mode, 0, ram)
    
        return ram, idx
    
    def equals_(self, arg1, arg1_mode, arg2, arg2_mode, arg3, arg3_mode, 
                ram, idx):
        arg1 = self._arg_eval(arg1, arg1_mode, ram)
        arg2 = self._arg_eval(arg2, arg2_mode, ram)
    
        if arg1 == arg2:
            ram = self._arg_write(arg3, arg3_mode, 1, ram)
        else:
            ram = self._arg_write(arg3, arg3_mode, 0, ram)
    
        return ram, idx
    
    def run_prog(self, code=None, reset=False, 
                 break_on_out=False, break_on_in=False):
        if code is not None:
            self.code = RAM(code)
        if reset:
            self.idx = 0

        while True:
            self.op, args_mode = self.get_op_and_arg_modes(self.code[self.idx])
            if self.op != '99':
                args_ = self.code[self.idx + 1: self.idx + self.idx_inc[self.op]]
            else:
                break
            args_and_modes = list(chain.from_iterable(zip(args_, args_mode)))
            self.code, new_idx = self.dispatch[self.op](*args_and_modes, 
                                                        self.code, self.idx)

            if new_idx == self.idx:
                self.idx += self.idx_inc[self.op]
            else:
                self.idx = new_idx

            if break_on_out and self.op == '04':
                break
            if break_on_in and self.op == '03':
                break


def calc_amps_output(code, phases):
    prev_amp = None
    for idx, phase in enumerate(phases):
        if idx == 0:
            intcomputer = IntcodeComputer(deque([0, phase]), deque())
        else:
            intcomputer = IntcodeComputer(deque([phase]), deque())
        if prev_amp:
            intcomputer.in_que.appendleft(prev_amp.out_que.pop())

        intcomputer.run_prog(code, reset=True)
        prev_amp = intcomputer
    return intcomputer.out_que.pop()


def calc_feedback_amps_output(code, phases):
    prev_amp = None

    amps = [IntcodeComputer(deque([phase]), deque(), id_) for id_, phase in enumerate(phases)]
    amps[0].in_que.appendleft(0)

    amps = cycle(amps)
    prev_amp = None
    current_amp = next(amps)
    while True:
        if prev_amp:
            current_amp.in_que.appendleft(prev_amp.out_que.pop())
        current_amp.run_prog(code)
        if all([each_amp.op == '99' for each_amp in amps]):
            return current_amp.out_que.pop()

        prev_amp = current_amp
        current_amp = next(amps)

# some tests from days 1-10 for the IntCode computer
intcomputer = IntcodeComputer(deque(), deque())
assert(('01', [1, 0, 0]) == intcomputer.get_op_and_arg_modes(101))
assert(('02', [0, 1, 0]) == intcomputer.get_op_and_arg_modes(1002))
assert(('03', [0]) == intcomputer.get_op_and_arg_modes(3))
assert(('04', [0]) == intcomputer.get_op_and_arg_modes(4))

test_code = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
test_out = deque()
intcomputer = IntcodeComputer(deque([7]), test_out)
intcomputer.run_prog(test_code, reset=True)
assert(intcomputer.out_que.pop() == 999)

test_code = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
intcomputer.in_que = deque([8])
intcomputer.run_prog(test_code, reset=True)
assert(intcomputer.out_que.pop() == 1000)

test_code = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
intcomputer.in_que =deque([9])
intcomputer.run_prog(test_code, reset=True)
assert(intcomputer.out_que.pop() == 1001)

test_code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
phases = [1,0,4,3,2]
for n_, each_phase in enumerate(phases):
    if n_ == 0:
        current_amp = IntcodeComputer(deque([0, each_phase]), deque())
    else:
        current_amp = IntcodeComputer(deque([prev_amp.out_que.pop(), each_phase]), 
                                      deque())
    current_amp.run_prog(test_code)
    prev_amp = current_amp
assert current_amp.out_que.pop() == 65210


code_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
phases_1 = [4, 3, 2, 1, 0]
assert(calc_amps_output(code_1, phases_1) == 43210)

code_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
phases_2 = [0, 1, 2, 3, 4]
assert(calc_amps_output(code_2, phases_2) == 54321)

code_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
phases_3 = [1,0,4,3,2]
assert(calc_amps_output(code_3, phases_3) == 65210)


code_4 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
intcomputer = IntcodeComputer(deque(), deque())
intcomputer.run_prog(code_4)
assert(list(intcomputer.out_que) == code_4[::-1])

code_5 = [1102,34915192,34915192,7,4,7,99,0]
intcomputer = IntcodeComputer(deque(), deque())
intcomputer.run_prog(code_5)
assert(len(str(intcomputer.out_que.pop())) == 16)

code_6 = [104,1125899906842624,99]
intcomputer = IntcodeComputer(deque(), deque())
intcomputer.run_prog(code_6)
assert(intcomputer.out_que.pop() == 1125899906842624)

