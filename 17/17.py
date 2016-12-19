from md5 import md5
from itertools import izip

moves = 'UDLR'
size = (4,4)
vaultpos = (3,3)
open_doors = 'bcdef'

def move_is_possible(position,d):
    if d=='U':
        return position[1]>0
    elif d=='D':
        return position[1] < size[1]-1
    elif d=='R':
        return position[0] < size[0]-1
    elif d=='L':
        return position[0]>0
        
def possible_moves(position, passcode, lastmoves):
    s = ''.join([passcode, lastmoves])
    h = md5(s).hexdigest()[:4]
    return (move for i,move in enumerate(moves)
            if move_is_possible(position, move) and h[i] in open_doors)

def make_move(pos, d):
    if d not in moves:
        raise TypeError('require direction to be in UDLR')
    elif d == 'U':
        return (pos[0],pos[1]-1)
    elif d == 'D':
        return (pos[0],pos[1]+1)
    elif d == 'R':
        return (pos[0]+1, pos[1])
    elif d=='L':
        return (pos[0]-1, pos[1])
        
def find_shortest_path(passcode, positions=None, step=0):
    if positions is None:
        positions = [((0,0), '')]
    next_positions = []
    for pos, pm in positions:
        #print "pos=",pos,'prev=', pm
        for move in possible_moves(pos, passcode, pm):
            #print move
            newpos = make_move(pos, move)
            npm = ''.join((pm, move))
            node = (newpos, npm)
            next_positions.append(node)
            if newpos == vaultpos:
                #valid_moves.append(npm)
                return npm
    if len(next_positions)==0:
        print 'No moves possible!'
        return positions
    return find_shortest_path(passcode, next_positions, step+1)

def find_longest_path(passcode, positions=None, step=0, longest_path=''):
    if positions is None:
        positions = [((0,0), '')]
    next_positions = []
    for pos, pm in positions:
        #print "pos=",pos,'prev=', pm
        for move in possible_moves(pos, passcode, pm):
            #print move
            newpos = make_move(pos, move)
            npm = ''.join((pm, move))
            node = (newpos, npm)
            if newpos == vaultpos:
                longest_path = npm
                continue
            next_positions.append(node)
    if len(next_positions)==0:
        print 'No moves possible!'
        return longest_path
    print step, len(longest_path)
    return find_longest_path(passcode, next_positions, step+1, longest_path)
        
if __name__ == '__main__':
    import sys
    passcode = sys.argv[1]
    print find_shortest_path(passcode)
    print find_longest_path(passcode)
