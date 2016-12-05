import numpy as np
from string import ascii_uppercase as letters

class Keypad(object):
    def __init__(self, starting_key=5):
        self.current_key = starting_key
        self.rows = self.set_rows()
        self.arows = np.array(self.rows)
        self.start_index = np.where(self.arows==self.current_key)
        self.current_index = self.start_index
        
        self.dirs = 'UDRL'
        self.mvi = [0,0,1,1]
        self.mvs = [-1,1,1,-1]
        self.minmax = [max, min, min, max]
        self.mm = [0, self.arows.shape[0]-1, self.arows.shape[1]-1, 0]
        
    def set_rows(self):
        return [[1,2,3],[4,5,6],[7,8,9]]

    def move(self, direction):
        if direction not in self.dirs:
            return
        i = self.dirs.find(direction)
        j = self.mvi[i]
        k = self.mvs[i]
        op = self.minmax[i]
        z = self.mm[i]
        
        cl = list(self.current_index)
        cl[j] = op(self.current_index[j]+k, z)
        t = tuple(cl)
        if self.arows[t] > 0:
            self.current_index = t
            
    def get_current_key(self):
        return self.arows[self.current_index].squeeze()

    def key_to_string(self, keyval):
        if keyval <10:
            return str(keyval)
        else:
            return letters[keyval-10]
            
    def process_string(self, strng):
        for char in strng:
            self.move(char)

    def get_code_from_file(self, fname):
        code = ''
        with open(fname) as thefile:
            for line in thefile:
                self.process_string(line)
                code += self.key_to_string(self.get_current_key())
        return code


class Keypad2(Keypad):
    def set_rows(self):
        return[[-1,-1,1,-1,-1],
               [-1,2,3,4,-1],
               [5,6,7,8,9],
               [-1,10,11,12,-1],
               [-1,-1,13,-1,-1]]
        
if __name__ == '__main__':
    import sys
    thefile = sys.argv[1]
    keypad = Keypad()
    code = keypad.get_code_from_file(thefile)
    print code
    keypad2 = Keypad2()
    code2 = keypad2.get_code_from_file(thefile)
    print code2
