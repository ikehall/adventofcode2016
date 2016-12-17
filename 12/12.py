

class Register(object):
    def __init__(self, num=0):
        self.reg = num
    def inc(self):
        self.reg += 1
    def dec(self):
        self.reg -= 1
    def __repr__(self):
        return str(self.reg)
        
def cpy(x,y):
    if isinstance(x, Register):
        y.reg = x.reg
    else:
        y.reg = int(x)

def jnz(x, y, instruction_set, lineno):
    if x > 0:
        return int(y)
    else:
        return 1

def run_line(line, registers, lineno, instruction_set):
    l = line.split()
    ins = l[0]
    if ins == 'cpy':
        x, y = l[1:]
        if x in registers:
            cpy(registers[x],registers[y])
        else:
            cpy(x, registers[y])
        return 1
    elif ins == 'inc':
        x = l[1]
        registers[x].inc()
        return 1 
    elif ins == 'dec':
        x = l[1]
        registers[x].dec()
        return 1
    elif ins == 'jnz':
        x,y = l[1:]
        if x in registers:
            return jnz(registers[x].reg, int(y), instruction_set, lineno)
        else:
            return jnz(int(x), int(y), instruction_set, lineno)
            
            
def run_script(instruction_set, register_set='abcd'):
    registers = {r:Register() for r in register_set}
    registers['c'].reg = 1
    lineno = 0
    while True:
        line = instruction_set[lineno].strip()
        lineno += run_line(line, registers, lineno, instruction_set)
        if lineno >= len(instruction_set):
            break
        #print registers
    print registers

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        instructions = thefile.readlines()
    print instructions
    run_script(instructions)
