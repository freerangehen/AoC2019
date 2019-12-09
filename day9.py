from itertools import chain, permutations, cycle
from collections import deque

code = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,20,0,1007,1101,0,197,1022,1102,475,1,1028,1102,30,1,1008,1101,25,0,1010,1102,1,23,1009,1101,0,22,1013,1101,470,0,1029,1102,24,1,1014,1102,1,39,1005,1101,31,0,1003,1101,807,0,1026,1101,0,26,1018,1102,1,804,1027,1101,0,0,1020,1102,1,38,1017,1101,0,27,1016,1102,443,1,1024,1101,0,36,1006,1102,21,1,1015,1101,28,0,1001,1102,33,1,1019,1102,1,37,1011,1102,1,190,1023,1101,0,434,1025,1101,34,0,1004,1102,1,1,1021,1101,0,29,1012,1102,1,32,1002,1101,35,0,1000,109,30,2105,1,-7,1001,64,1,64,1105,1,199,4,187,1002,64,2,64,109,-23,2101,0,-5,63,1008,63,32,63,1005,63,225,4,205,1001,64,1,64,1105,1,225,1002,64,2,64,109,7,2102,1,-5,63,1008,63,23,63,1005,63,251,4,231,1001,64,1,64,1106,0,251,1002,64,2,64,109,-16,2101,0,2,63,1008,63,33,63,1005,63,275,1001,64,1,64,1106,0,277,4,257,1002,64,2,64,109,10,21102,40,1,4,1008,1012,40,63,1005,63,299,4,283,1106,0,303,1001,64,1,64,1002,64,2,64,109,7,2102,1,-9,63,1008,63,33,63,1005,63,327,1001,64,1,64,1105,1,329,4,309,1002,64,2,64,109,-17,2107,34,2,63,1005,63,347,4,335,1105,1,351,1001,64,1,64,1002,64,2,64,109,1,1201,8,0,63,1008,63,23,63,1005,63,375,1001,64,1,64,1106,0,377,4,357,1002,64,2,64,109,-4,2108,31,8,63,1005,63,395,4,383,1105,1,399,1001,64,1,64,1002,64,2,64,109,3,1201,8,0,63,1008,63,36,63,1005,63,421,4,405,1105,1,425,1001,64,1,64,1002,64,2,64,109,25,2105,1,1,4,431,1001,64,1,64,1105,1,443,1002,64,2,64,109,-3,1205,0,459,1001,64,1,64,1106,0,461,4,449,1002,64,2,64,109,-2,2106,0,10,4,467,1106,0,479,1001,64,1,64,1002,64,2,64,109,12,1206,-9,495,1001,64,1,64,1106,0,497,4,485,1002,64,2,64,109,-39,1207,9,36,63,1005,63,519,4,503,1001,64,1,64,1105,1,519,1002,64,2,64,109,11,1202,-1,1,63,1008,63,28,63,1005,63,541,4,525,1105,1,545,1001,64,1,64,1002,64,2,64,109,6,2107,24,1,63,1005,63,565,1001,64,1,64,1106,0,567,4,551,1002,64,2,64,109,1,1207,-3,35,63,1005,63,583,1106,0,589,4,573,1001,64,1,64,1002,64,2,64,109,1,21102,41,1,5,1008,1015,40,63,1005,63,613,1001,64,1,64,1105,1,615,4,595,1002,64,2,64,109,-2,2108,22,1,63,1005,63,635,1001,64,1,64,1105,1,637,4,621,1002,64,2,64,109,-10,1208,4,33,63,1005,63,653,1106,0,659,4,643,1001,64,1,64,1002,64,2,64,109,16,1206,6,673,4,665,1106,0,677,1001,64,1,64,1002,64,2,64,109,-4,1202,-8,1,63,1008,63,35,63,1005,63,701,1001,64,1,64,1105,1,703,4,683,1002,64,2,64,109,13,21108,42,42,-8,1005,1015,721,4,709,1105,1,725,1001,64,1,64,1002,64,2,64,109,-18,21107,43,44,5,1005,1010,743,4,731,1106,0,747,1001,64,1,64,1002,64,2,64,109,-11,1208,8,32,63,1005,63,765,4,753,1106,0,769,1001,64,1,64,1002,64,2,64,109,15,21101,44,0,5,1008,1014,47,63,1005,63,789,1105,1,795,4,775,1001,64,1,64,1002,64,2,64,109,13,2106,0,5,1106,0,813,4,801,1001,64,1,64,1002,64,2,64,109,-12,21108,45,43,0,1005,1010,829,1106,0,835,4,819,1001,64,1,64,1002,64,2,64,109,-4,21107,46,45,10,1005,1016,855,1001,64,1,64,1106,0,857,4,841,1002,64,2,64,109,3,21101,47,0,5,1008,1014,47,63,1005,63,883,4,863,1001,64,1,64,1106,0,883,1002,64,2,64,109,10,1205,2,901,4,889,1001,64,1,64,1105,1,901,4,64,99,21102,27,1,1,21102,915,1,0,1106,0,922,21201,1,13433,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,22102,1,1,-1,21201,-2,-3,1,21102,1,957,0,1105,1,922,22201,1,-1,-2,1106,0,968,21202,-2,1,-2,109,-3,2106,0,0
]

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

    def __init__(self, in_que, out_que, id_=None):
        self.in_que = in_que
        self.out_que = out_que
        self.idx = 0
        self.op = None
        self.id_ = id_
        self.last_input = None
        self.wait_for_input = False
        self.relative_base = 0
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
    
    def run_prog(self, code, reset=False, 
                 break_on_out=False, break_on_in=False):
        code = RAM(code)
        if reset:
            self.idx = 0

        while True:
            self.op, args_mode = self.get_op_and_arg_modes(code[self.idx])
            if self.op != '99':
                args_ = code[self.idx + 1: self.idx + self.idx_inc[self.op]]
            else:
                break
            args_and_modes = list(chain.from_iterable(zip(args_, args_mode)))
            code, new_idx = self.dispatch[self.op](*args_and_modes, code, self.idx)

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



if __name__ == "__main__":
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

    # part I input is [1]
    # part II intput is [2]
    intcomputer = IntcodeComputer(deque([2]), deque())
    intcomputer.run_prog(code)
    print(intcomputer.out_que)
