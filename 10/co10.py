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

        #got a value
        else:
            vals += tpl

        #If we have 2 values, and know who to pass them off to,
        #do so immediately!
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
            _,n,_,_,_,bol,nl,_,_,_,boh,nh = l
            bots[n] = cobot(n)
            if bol == 'bot':
                bots[nl] = cobot(nl)
            else:
                outputs[nl] = output(nl, sink if nl in op_to_track else None)
            if boh == 'bot':
                bots[nh] = cobot(nh)
            else:
                outputs[nh] = output(nh, sink if nh in op_to_track else None)
        else:
            n = l[-1]
            bots[n] = cobot(n)
    return bots, outputs

def link_and_initialize_bots(instruction_set, bots, outputs):
    #This should also start the bots going as well.
    #They are coroutines, and thus have a mind of their own.
    for line in instruction_set:
        l = line.split()
        if l[0] == 'bot':
            _,t,_,_,_,bol,nl,_,_,_,boh,nh=l
            target = bots[t]
            low = bots[nl] if bol=='bot' else outputs[nl]
            hi = bots[nh] if boh=='bot' else outputs[nh]
            target.send([low, hi])
        else:
            _,v,_,_,_,n=l
            value = [v]
            target = bots[n]
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
    bots, outputs = initialize_cobots(l,s)
    link_and_initialize_bots(l, bots, outputs)
