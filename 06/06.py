import numpy as np
from scipy.stats import mode, itemfreq

def error_correction(lines):
    alines = np.array(lines, dtype='c')
    return ''.join(list(mode(alines, axis=0)[0].squeeze()))

def least_freq(lines):
    alines = np.array(lines, dtype='c').T
    return ''.join([itemfreq(col)[np.argmin(itemfreq(col)[:,1]),0]
                    for col in alines])
    

if __name__ =='__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        lines = [l.strip() for l in thefile]
        print error_correction(lines)
        print least_freq(lines)
