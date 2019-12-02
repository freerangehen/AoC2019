
code_ =[1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,6,19,23,2,23,6,27,1,5,27,31,1,31,9,35,2,10,35,39,1,5,39,43,2,43,10,47,1,47,6,51,2,51,6,55,2,55,13,59,2,6,59,63,1,63,5,67,1,6,67,71,2,71,9,75,1,6,75,79,2,13,79,83,1,9,83,87,1,87,13,91,2,91,10,95,1,6,95,99,1,99,13,103,1,13,103,107,2,107,10,111,1,9,111,115,1,115,10,119,1,5,119,123,1,6,123,127,1,10,127,131,1,2,131,135,1,135,10,0,99,2,14,0,0]



def add_(loc1, loc2, res_loc, ram):
    ram[ram[res_loc]] = ram[ram[loc1]] + ram[ram[loc2]]
    return ram

def mul_(loc1, loc2, res_loc, ram):
    ram[ram[res_loc]] = ram[ram[loc1]] * ram[ram[loc2]]
    return ram


dispatch = {1: add_, 
            2: mul_}

if __name__ == "__main__":
    for n in range(101):
        for m in range(101):
            code = code_.copy()
            code[1] = n
            code[2] = m
            idx = 0
            while idx < len(code):
                op = code[idx]
                if op == 99:
                    idx += 1
                    if code[0] == 19690720:
                        print(n, m)
                        break
                else:
                    code = dispatch[op](idx+1,idx+2, idx+3, code)
                    idx += 4

