def find_min(list_of_exclusions, mini=0):
    while True:
        l = len(list_of_exclusions)
        remove = False
        for excl in list_of_exclusions:
            if excl[0]<=mini and excl[1]>mini:
                mini = excl[1]+1
                remove = True
                break
        if remove:
            list_of_exclusions.remove(excl)
            #print excl
        if len(list_of_exclusions) == l:
            break
    return mini
        
def make_list_of_exclusions(lines):
    return [map(int, line.strip().split('-')) for line in lines]

def combine_exclusions(excls):
    sorted_excls = sorted(excls)
    maxn = 4294967295+1
    cmin, cmax = sorted_excls.pop(0)
    new_exclusions = []
    while True:
        try:
            e2 = sorted_excls.pop(0)
        except IndexError:
            new_exclusions.append((cmin,cmax))
            new_exclusions.append((maxn, maxn))
            return new_exclusions
        if e2[0]<=cmax+1:
            cmax = e2[1] if e2[1]>cmax else cmax
        else:
            new_exclusions.append((cmin, cmax))
            cmin = e2[0]
            cmax = e2[1]

def count_inclusions(combined_sorted_exclusions):
    l = combined_sorted_exclusions
    return sum(y[0]-x[1]-1 for x,y in zip(l[:-1],l[1:]))


    
if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        excls = make_list_of_exclusions(thefile.readlines())
        new_excls = combine_exclusions(excls)
        print "part 2(number of ips allowed)=%d"%(count_inclusions(new_excls))
        print "part 1(minimum ip)=%d"%find_min(excls)
