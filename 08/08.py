import numpy as np

def turn_on_rect(array, rect_size, start=(0,0)):
    array[start[0]:start[0]+rect_size[0],start[1]:start[1]+rect_size[1]]=True

def rotate_row(array, rownum, rotatenum):
    array[rownum,:] = np.roll(array[rownum,:], rotatenum)

def rotate_column(array, colnum, rotatenum):
    array[:,colnum] = np.roll(array[:,colnum], rotatenum)

def read_instruction(ins, array):
    i0 = ins.split()
    if i0[0]=='rect':
        width,height=(int(x) for x in i0[1].split('x'))
        turn_on_rect(array, (height, width))
    elif i0[0] == 'rotate':
        row_or_col_num = int(i0[2].split('=')[1])
        rotatenum = int(i0[4])
        if i0[1]=='column':
            rotate_column(array, row_or_col_num, rotatenum)
        else:
            rotate_row(array, row_or_col_num, rotatenum)
        
def pretty_print(array):
    for row in array:
        print ''.join('#' if x else '.' for x in row)
            

if __name__ == '__main__':
    import sys
    array = np.zeros((6,50), dtype=bool)
    #array = np.zeros((3,7), dtype=bool)
    with open(sys.argv[1]) as instructions:
        for instruction in instructions:
            read_instruction(instruction.strip(), array)
    print np.sum(array)
    pretty_print(array)
