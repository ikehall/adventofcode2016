import numpy as np
def disc_times(num, pos_at_t0, period, maxT):
    first_time = -(num+1)+(-pos_at_t0%period)
    while first_time <0:
        first_time += period
    return set(np.arange(maxT/period, dtype=int)*period+first_time)

def decode_disc(line):
    return int(line.split()[3]), int(line.strip().strip('.').split()[-1])
    
if __name__=='__main__':
    import sys
    discs = []
    with open(sys.argv[1]) as thefile:
        for n, line in enumerate(thefile):
            period, pos_at_t0 = decode_disc(line)
            discs.append([n,pos_at_t0, period])
    maxT = np.product(np.array(discs)[:,2])

    print set.intersection(*[disc_times(disc[0], disc[1], disc[2], maxT) for disc in discs])
