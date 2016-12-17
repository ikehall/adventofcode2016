from md5 import md5

def hashfunc1(s):
    return md5(s).hexdigest()

def hashfunc2(s):
    news = s
    for i in range(2017):
        news = md5(news).hexdigest()
    return news
    
def potential_key_generator(salt):
    index = 0
    while True:
        s = salt+str(index)
        yield hashfunc2(s), index
        index += 1

def has_triple(pot_key):
    chrs = ''
    for char in pot_key:
        if pot_key.find(char*3) >= 0:
            return char
    return chrs

def has_quint(pot_key, char):
    return pot_key.find(char*5)>=0


def get_keys(salt):
    potential_keys = {}
    confirmed_keys = {}
    for pot_key, index in potential_key_generator(salt):
        c = has_triple(pot_key)
        if c:
            potential_keys[pot_key] = [0, c, index]

        keys_to_pop = []
        for test_key,(count, char, ind0) in potential_keys.iteritems():
            if test_key == pot_key:
                continue
            if has_quint(pot_key, char):
                confirmed_keys[test_key] = ind0
                keys_to_pop.append(test_key)
                print test_key, pot_key, ind0, index, count, char, len(confirmed_keys)
            else:
                if count > 1000:
                    keys_to_pop.append(test_key)
                potential_keys[test_key][0]+=1
                
        for test_key2pop in keys_to_pop:
            potential_keys.pop(test_key2pop)
        
        if len(confirmed_keys) >= 70:
            return sorted(confirmed_keys.values())
        
            
if __name__ == '__main__':
    import sys
    print get_keys(sys.argv[1])[64]  ###THEY MADE A MIS-STEAK (or maybe i did)
                                     ###THIS IS THE 65th key
