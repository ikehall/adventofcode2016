import numpy as np
turns = 'LR'
headings = 'NESW'
x_comps = [0,1,0,-1]
y_comps = [1,0,-1,0]

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return np.sqrt((self.x-other.x)**2+(self.y-other.y)**2)

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

    def __repr__(self):
        return ''.join(['(',str(self.x),',', str(self.y), ')'])
        
class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return ''.join(['<',self.p1.__repr__(),'-',self.p2.__repr__(),'>'])
        
    def _abc(self):
        a = self.p2.y-self.p1.y
        b = self.p2.x-self.p1.x
        c = a*self.p1.x + b*self.p1.y
        return a,b,c

    def point_on_line(self, point):
        d1 = point.dist(self.p1)
        d2 = point.dist(self.p2)
        dl = self.p1.dist(self.p2)
        return dl == d1+d2
        
    def intersection(self, other_line):
        a1,b1,c1 = self._abc()
        a2,b2,c2 = other_line._abc()
        det = a1*b2-a2*b1
        if det == 0:
            #lines are parallel...check for either endpoint of other_line
            #residing inside this line.  If one or both do, return the point
            #that is closest to self.p1
            closest = None
            if self.point_on_line(other_line.p1):
                closest = other_line.p1
            if self.point_on_line(other_line.p2):
                if closest is None:
                    closest = other_line.p2
                else:
                    d1 = self.p1.dist(other_line.p1)
                    d2 = self.p2.dist(other_line.p2)
                    closest = other_line.p1 if d1<d2 else other_line.p2
            return closest
        xi = (b2*c1-b1*c2)/det
        yi = (a1*c2-a2*c1)/det
        #Make sure xi,yi lies between the endpoints
        minx = min(self.p1.x, self.p2.x)
        maxx = max(self.p1.x, self.p2.x)
        miny = min(self.p1.y, self.p2.y)
        maxy = max(self.p1.y, self.p2.y)
        minx2 = min(other_line.p1.x, other_line.p2.x)
        maxx2 = max(other_line.p1.x, other_line.p2.x)
        miny2 = min(other_line.p1.y, other_line.p2.y)
        maxy2 = max(other_line.p1.y, other_line.p2.y)
        if minx <= xi <= maxx and miny <= yi <= maxy and minx2 <= xi <= maxx2 and miny2 <= yi <= maxy2:
            return Point(xi, yi)
        return None
            

def get_xy(heading):
    assert heading in headings
    i = headings.find(heading)
    return np.array([x_comps[i],y_comps[i]])

def turn(direction, heading):
    j = turns.find(direction.upper())
    t = -1 if j==0 else 1
    i = headings.find(heading.upper())
    newi = (i+t)%len(headings)
    return headings[newi]
    
def vector_dist(turn_dir, dist_trav, begin_heading):
    assert turn_dir in turns
    new_heading = turn(turn_dir, begin_heading)
    return new_heading, int(dist_trav)*get_xy(new_heading)


def process_instructions(instruction_set, begin_heading='N'):
    iset = instruction_set.split(',')
    h = begin_heading
    v = np.zeros(2, dtype=int)
    for ins in iset:
        turn_dir = ins.strip()[0]
        dist = int(ins.strip()[1:])
        h, nv = vector_dist(turn_dir, dist, h)
        v += nv
    return v

def find_first_repeat_location(instruction_set, begin_heading='N'):
    iset = instruction_set.split(',')
    h = begin_heading
    v = np.zeros(2, dtype=int)
    locs = [Point(0,0)]
    for ins in iset:
        turn_dir = ins.strip()[0]
        dist = int(ins.strip()[1:])
        h, nv = vector_dist(turn_dir, dist, h)
        v += nv
        t = tuple(v)
        p = Point(*t)
        if p not in locs:
            locs.append(p)
        else:
            return p
        if len(locs) > 3:
            this_line = Line(locs[-2], locs[-1])
            for i in range(1,len(locs)-2):
                test_line = Line(locs[i-1],locs[i])
                intpnt=this_line.intersection(test_line)
                if intpnt is not None:
                    return intpnt
        
                    
    
if __name__=='__main__':
    import sys
    instructions = sys.argv[1]
    with open(instructions) as f:
        s = f.readlines()
    ss = ''.join(s)
    v = process_instructions(ss)
    print v, abs(v[0])+abs(v[1])
    v1 = find_first_repeat_location(ss)
    print v1, abs(v1.x)+abs(v1.y)
