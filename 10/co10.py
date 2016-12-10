from operator import mul

#Solving with coroutines!!!
def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

@coroutine
def output(num, final_target=None):
    val = []
    try:
        while True:
            newval = (yield)
            val.append(newval[0])
    except GeneratorExit:
        if final_target is not None:
            final_target.send(val)
        
@coroutine
def cobot(num):
    hi = None
    lo = None
    vals = []
    while True:
        tpl = (yield)

        #Got a pair of bots to send hi and lo values
        if len(tpl) == 2:
            lo, hi = tpl
        else:
            vals += tpl

        #Got a value
        if len(vals) == 2 and lo is not None:
            vl, vh = sorted(int(x) for x in vals)
            #Print the result needed for part 1
            if vl==17 and vh==61:
                print "hi, I'm cobot #%s.  I have values %d and %d"%(num,vl,vh)
            lo.send([str(vl)])
            hi.send([str(vh)])
            
def initialize_cobots(instruction_set, sink):
    bots = {}
    outputs = {}
    op_to_track = ['0','1','2']
    for line in instruction_set:
        l = line.split()
        if l[0]=='bot':
            bots[l[1]] = cobot(l[1])
            if l[5] == 'bot':
                bots[l[6]] = cobot(l[6])
            else:
                outputs[l[6]] = output(l[6]) if l[6] not in op_to_track else output(l[6], sink)
            if l[-2] == 'bot':
                bots[l[-1]] = cobot(l[-1])
            else:
                outputs[l[-1]] = output(l[-1]) if l[-1] not in op_to_track else output(l[-1], sink)
        else:
            bots[l[-1]] = cobot(l[-1])
    return bots, outputs

def link_and_initialize_bots(instruction_set, bots, outputs):
    #This should also start the bots going as well.
    #They are coroutines, and thus have a mind of their own.
    for line in instruction_set:
        l = line.split()
        if l[0] == 'bot':
            target = bots[l[1]]
            low = bots[l[6]] if l[5]=='bot' else outputs[l[6]]
            hi = bots[l[-1]] if l[-2]=='bot' else outputs[l[-1]]
            target.send([low, hi])
        else:
            value = [l[1]]
            target = bots[l[-1]]
            target.send(value)
    for o in outputs:
        outputs[o].close()

@coroutine
def multiplier_sink():
    vals=[]
    for i in range(3):
        newval = (yield)
        vals+=[int(v) for v in newval]
    v = reduce(mul, vals,1)
    print 'Final count of bins: ', v

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        l = thefile.readlines()
    s = multiplier_sink()
    print 'initalizing'
    bots, outputs = initialize_cobots(l,s)
    print 'linking'
    link_and_initialize_bots(l, bots, outputs)
