import itertools
import string

def get_checksum(s):
    return s[s.find('[')+1:s.find(']')]

def get_sector(s):
    return int(s[s.rfind('-')+1:s.find('[')])

def get_encrypted_name(s):
    return s[:s.rfind('-')]
    
def make_checksum(s):
    n = get_encrypted_name(s)
    counts = sorted([(k,len(list(g))) for k,g in itertools.groupby(sorted(n))
                     if k in string.letters],
                    key=lambda x: x[1], reverse=True)
    return ''.join([x[0] for x in counts[:5]])
        
def is_valid(s):
    return make_checksum(s)==get_checksum(s)

def let_to_num(l):
    return string.ascii_lowercase.find(l)

def num_to_let(n):
    return string.ascii_lowercase[n%26]
    
def decrypt_name(name_string, sector):
    return ' '.join([''.join([num_to_let(let_to_num(x)+sector)
                                        for x in s])
                               for s in name_string.split('-')])
def decrypt_string(s):
    return decrypt_name(get_encrypted_name(s), get_sector(s))
    
if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    sector_sum = 0
    with open(fname) as thefile:
        for s in thefile:
            if is_valid(s):
                sector_sum += get_sector(s)
                d = decrypt_name(s, get_sector(s))
                if 'north' in d:
                    print decrypt_string(s), get_sector(s)
    print sector_sum
