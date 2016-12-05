import numpy as np

def valid_triangle(side_lengths):
    sides = list(side_lengths)
    longest = sides.pop(sides.index(max(side_lengths)))
    remaining = 0
    for side in sides:
        remaining += side
    if remaining > longest:
        return True
    return False

def count_valid(fname):
    valid = 0
    invalid = 0
    with open(fname) as thefile:
        for line in thefile:
            sides = [int(x) for x in line.split()]
            if valid_triangle(sides):
                valid += 1
            else:
                invalid += 1
    return valid, invalid

def count_valid2(fname):
    valid = 0
    invalid = 0
    r = []
    with open(fname) as thefile:
        for line in thefile:
            r.append([int(x) for x in line.split()])
    newr = np.array(r).T
    new_tris = []
    for col in newr:
        new_t = [col[i:i+3] for i in range(0, len(col), 3)]
        for t in new_t:
            new_tris.append(t)
    for triangle in new_tris:
        if valid_triangle(triangle):
            valid += 1
        else:
            invalid += 1
            
    return valid, invalid
    
if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    v, i = count_valid(fname)
    print v, i
    v1, i1 = count_valid2(fname)
    print v1, i1
    
