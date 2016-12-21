import numpy as np
from io import StringIO

swap_names = ['swap','pos_or_let','X','with','pos_or_let2','Y']
rotate_lr_names = ['rotate','direction','X','steps']
rotate_pos_names = ['rotate','based','on','pos','of','let','X']
reverse_names = ['reverse','pos','X','through','Y']
move_names = ['move','pos','X','to','pos2','Y']

def vars_from_instruction(instruction, names):
    return np.genfromtxt(StringIO(unicode(instruction)),
                         dtype=None,
                         names=names)

def execute(instruction, password):
    first,second = instruction.split()[:2]
    if first == 'swap':
        var = vars_from_instruction(instruction, swap_names)
        if second=='position':
            return swap_xy(password,int(var['X']),int(var['Y']))
        else:
            return swap_Lxy(password, var['X'],var['Y'])
    elif first == 'rotate':
        if second == 'based':
            var = vars_from_instruction(instruction, rotate_pos_names)
            return rotate_based_on_x(password, var['X'])
        else:
            var = vars_from_instruction(instruction, rotate_lr_names)
            return rotateX(password, int(var['X']), var['direction'])
    elif first == 'reverse':
        var = vars_from_instruction(instruction, reverse_names)
        return reverse_xy(password, int(var['X']),int(var['Y']))
    else:
        var = vars_from_instruction(instruction, move_names)
        return move_xy(password, int(var['X']),int(var['Y']))

def execute_adjoint(instruction, password):
    print password, instruction
    first, second = instruction.split()[:2]
    if first == 'swap':
        #Both swaps are their own adjoint...so nothing changes here
        var = vars_from_instruction(instruction, swap_names)
        if second=='position':
            return swap_xy(password,int(var['X']),int(var['Y']))
        else:
            return swap_Lxy(password, var['X'],var['Y'])
    elif first =='rotate':
        if second=='based':
            var = vars_from_instruction(instruction, rotate_pos_names)
            return unrotate_based_on_x(password, var['X'])
            #This is the tricky adjoint.
            #In the original,
            #Original position, new positon
            #0 --> 1 (1 step)             (rev by -1 steps)
            #1 --> 3 (2 steps)            (rev by -2 steps)
            #2 --> 5 (3 steps)            (rev by -3 steps)
            #3 --> 7 (4 steps)            (rev by -4 steps)
            #4 --> 2 (6 steps) (-2 steps) (rev by 2 steps)
            #5 --> 4 (7 steps) (-1 steps) (rev by 1 step)
            #6 --> 6 (8 steps) (identity) (rev by 0 steps)
            #7 --> 0 (9 steps) (1 step)   (rev by -1 steps)
        else:
            #This adjoint is itself with negative step values
            var = vars_from_instruction(instruction, rotate_lr_names)
            return rotateX(password, -int(var['X']), var['direction'])
    elif first == 'reverse':
        #This is also it's own adjoint
        var = vars_from_instruction(instruction, reverse_names)
        return reverse_xy(password, int(var['X']), int(var['Y']))
    else:
        #The move adjoint should simply be swapping x and y
        var = vars_from_instruction(instruction, move_names)
        return move_xy(password, int(var['Y']), int(var['X']))
            
def toarray(s):
    return np.array(s,dtype='c')

def swap_xy(s,x,y):
    sa = toarray(s)
    sa[x],sa[y] = sa[y],sa[x]
    return sa.tostring()

def swap_Lxy(s,x,y):
    sa = toarray(s)
    mx = (sa==x)
    my = (sa==y)
    sa[mx] = y
    sa[my] = x
    return sa.tostring()

def rotateX(s, steps, direction):
    if direction=='left':
        steps = -steps
    return np.roll(toarray(s),steps).tostring()

def rotate_based_on_x(s,x):
    i = s.find(x)
    steps = 1 + i + int(i>3)
    return rotateX(s,steps,'right')

unrotate_map = {0:-1,
                1:-1,
                2:2,
                3:-2,
                4:1,
                5:-3,
                6:0,
                7:-4}
    
def unrotate_based_on_x(s,x):
    i = s.find(x)
    steps = unrotate_map[i]
    return rotateX(s, steps, 'right')
    
    
def reverse_xy(s,x,y):
    sa = toarray(s)
    sa[x:y+1] = sa[y::-1] if x==0 else sa[y:x-1:-1]
    return sa.tostring()

def move_xy(s,x,y):
    l = list(s)
    c = l.pop(x)
    l.insert(y,c)
    return ''.join(l)

if __name__ == '__main__':
    import sys
    password = sys.argv[2]
    with open(sys.argv[1]) as thefile:
        lines = thefile.readlines()
    for line in lines:
        password = execute(line.strip(), password)
    print password
    newpassword = sys.argv[3]
    for line in reversed(lines):
        newpassword = execute_adjoint(line.strip(), newpassword)
        print newpassword
    print newpassword
    
    
