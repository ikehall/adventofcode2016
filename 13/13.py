from collections import Counter
from itertools import product

def isWall(x,y, favorite_number):
    num = x*x + 3*x + 2*x*y + y + y*y + favorite_number
    c = Counter(bin(num)[2:])
    return c['1']%2
        
def valid_moves(x,y, favorite_number, pos_visited):
    for xp, yp in product((1,0,-1), (1,0,-1)):
        if abs(xp) == abs(yp):
            continue
        xx,yy = x+xp, y+yp
        if xx<0 or yy<0 or isWall(xx,yy,favorite_number) or (xx,yy) in pos_visited:
            continue
        yield xx,yy

def take_steps(positions, favorite_number, final_position, num_moves = 0, positions_visited=None):
    if positions_visited is None:
        positions_visited = set()
    print "step %d, nodes visited=%d"%(num_moves, len(positions_visited))
    next_positions = set()
    for pos in positions:
        x,y = pos
        moves_to_test = valid_moves(x, y, favorite_number, positions_visited)
        for mv in moves_to_test:
            #print mv
            positions_visited.add(mv)
            next_positions.add(mv)
            if final_position in positions_visited:
                return None, num_moves + 1, None
    return next_positions, num_moves+1, positions_visited
    #return take_steps(next_positions, favorite_number,
    #                  final_position, num_moves+1, positions_visited)

if __name__ == '__main__':
    import sys
    fav_num = int(sys.argv[1])
    start_pos= ((1,1),)
    n = 0
    final_pos = (31,39)
    pv = None
    pv50 = 0
    while True:
        start_pos, n, pv = take_steps(start_pos, fav_num, (31,39), n, pv)
        if start_pos is None:
            break
        if n == 50:
            p50 = len(pv)
    print n
    print p50
    
