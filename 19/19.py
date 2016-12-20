import numpy as np
from numba import jit

@jit(nopython=True)
def find_first(item, vec):
    for i in xrange(len(vec)):
        if item==vec[i]:
            return i
    return -1

def one_round(numbers):
    position_with_presents = np.arange(len(numbers), dtype='i8')
    mask = (position_with_presents%2==0)
    #capture the action (or inaction) of the last person
    mask[0] = len(position_with_presents)%2==0
    return numbers[mask]

def all_rounds(n):
    players = np.arange(int(n), dtype='i8')
    while len(players) > 1:
        players = one_round(players)
    return players

#Part2
class Node(object):
    def __init__(self, n):
        self.n = n
        self.left = None
        self.right = None

    def __hash__(self):
        return hash(self.n)

        
class CircleJerks(object):
    def __init__(self, number):
        nodelist = []
        nodelist.append(Node(0))
        for i in xrange(number-1):
            nodelist.append(Node(i+1))
        nodelist[0].right=nodelist[-1]
        nodelist[-1].left = nodelist[0]
        for i in xrange(number-1):
            nodelist[i].left = nodelist[i+1]
            nodelist[i+1].right = nodelist[i]
        self.current = nodelist[0]
        self.across = nodelist[number/2]
        self.alternator = 0 if number%2==0 else 1
        self.n = number
        
        
    def steal(self):
        self.current=self.current.left
        self.across.right.left = self.across.left
        self.across.left.right = self.across.right
        for i in xrange(self.alternator+1):
            self.across = self.across.left
        self.alternator = (self.alternator+1)%2
        self.n -= 1

def let_the_circle_jerks_do_their_thing(n):
    c = CircleJerks(int(n))
    while c.n > 1:
        c.steal()
    return c.current.n


    
if __name__ == '__main__':
    import sys
    print all_rounds(sys.argv[1])+1
    print let_the_circle_jerks_do_their_thing(int(sys.argv[1]))+1
