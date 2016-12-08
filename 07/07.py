def has_abba(s):
    def is_abba(ss):
        return ss[:2]==ss[-1:1:-1] and ss[0]!=ss[1]
    for i in range(len(s)-3):
        if is_abba(s[i:i+4]):
            return True
    return False

def all_aba(s):
    def is_aba(ss):
        #print ss
        return ss==ss[::-1] and ss[0]!=ss[1]
    #aba = [s[i:i+3] for i in range(len(s)-2) if is_aba(s[i:i+3])]
    aba=[]
    for i in range(len(s)-2):
        if is_aba(s[i:i+3]):
            aba.append(s[i:i+3])
    return aba
    
def split_by_brackets(s):
    openmask = map(lambda c:c=='[',s)
    closemask = map(lambda c:c==']',s)
    openindicies = [i for i,m in enumerate(openmask) if m]
    closeindicies = [i for i,m in enumerate(closemask) if m]
    not_in_brackets=[]
    in_brackets = []
    lastclose = 0
    for i,br in enumerate(openindicies):
        not_in_brackets.append(s[lastclose:br])
        lastclose=closeindicies[i]
        in_brackets.append(s[br+1:lastclose])
    not_in_brackets.append(s[lastclose+1:])
    return not_in_brackets, in_brackets
    
def supports_TLS(s):
    ob, ib = split_by_brackets(s.strip())
    #print ib, ob
    #print [has_abba(ss) for ss in ib]
    return any(has_abba(ss) for ss in ob) and not any(has_abba(ss) for ss in ib)

def supports_SSL(s):
    ob, ib = split_by_brackets(s.strip())
    aba = []
    bab = []
    for ss in ob:
        aba += all_aba(ss)
    for ss in ib:
        bab += all_aba(ss)
    #print aba, bab
    for test_aba in aba:
        for test_bab in bab:
            #print test_aba, test_bab
            if test_aba[0]==test_bab[1] and test_aba[1]==test_bab[0]:
                return True
    return False
    
if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        
        print sum(map(supports_TLS,thefile))
        thefile.seek(0)
        print sum(map(supports_SSL,thefile))
