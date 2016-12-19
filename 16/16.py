from itertools import izip_longest

def dragon_curve(data):
    b = data[::-1]
    return '0'.join([data,''.join(str(abs(int(c)-1)) for c in b)])

def fill_disk(data, length):
    new_data = data
    while len(new_data) < length:
        print 'making new data %d'%len(new_data)
        new_data = dragon_curve(new_data)
    print 'made new data %d'%len(new_data)
    return new_data[:length]

def str_not_xor(pair):
    return str( 1-(int(pair[0])^int(pair[1])) )

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)]*n
    return izip_longest(*args, fillvalue=fillvalue)

def checksum(data):
    return ''.join(str_not_xor(pair) for pair in grouper(data,2))

def make_checksum(data):
    cs = checksum(data)
    while len(cs)%2==0:
        print 'making checksum %d'%len(cs)
        cs = checksum(cs)
    print 'made checksum %d'%len(cs)
    return cs
    
if __name__ == '__main__':
    import sys
    init_state = sys.argv[1]
    fill_length = int(sys.argv[2])
    print make_checksum(fill_disk(init_state, fill_length))
