def is_trap(triplet):
    l,c,r = triplet
    return c&(l^r) or (l&(l^(r or c))) or (r&(r^(l or c)))

def char_for_line(triplet):
    return '^' if is_trap(triplet) else '.'

def line_to_bool(s):
    return [True if c=='^' else False for c in s]
    
def next_line(line):
    bool_line = line_to_bool(''.join(['.',line.strip(),'.']))
    lcrgen = ((bool_line[i], c, bool_line[i+2])
              for i,c in enumerate(bool_line[1:-1]))
    newline = ''.join(char_for_line(triplet) for triplet in lcrgen)
    return newline

def gen_lines(line, n):
    lines = [line]
    for i in range(n-1):
        lines.append(next_line(lines[-1]))
    #print lines
    return lines

def count_safe(lines):
    return ''.join(lines).count('.')

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        l = thefile.readline()
    print count_safe(gen_lines(l, int(sys.argv[2])))
    
    
