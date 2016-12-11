from operator import mul
from collections import defaultdict

#Solving with coroutines!!!
#Each bot or output is a coroutine.  They expect to be sent dictionaries
#whenever an action happens.  Those dictionaries will have keys of either
#num, val, hi, lo for bots and num, val, target for outputs.  They will then
#do something with the appropriate items.  When bots have 2 chips AND
#the instructions they need to send their two chips to the next bot, they
#will do so automagically.

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

@coroutine
def output():
    val = []
    num = target = None
    try:
        while True:
            dct = (yield)
            num = dct.get('num', None) if num is None else num
            v = dct.get('val', None)
            if v is not None:
                val.append(v)
            target = dct.get('target', None) if target is None else target
    except GeneratorExit:
        if target is not None:
            target.send(val)
        
@coroutine
def cobot():
    num = hi = lo = None
    vals = []
    while True:
        dct = (yield)
        num = dct.get('num', None) if num is None else num
        hi = dct.get('hi', None) if hi is None else hi
        lo = dct.get('lo', None) if lo is None else lo
        v = dct.get('val', None)
        if v is not None: vals.append(v)
        #If we have 2 values, and know who to pass them off to,
        #do so immediately!
        if len(vals) == 2 and lo is not None:
            vl, vh = sorted(int(x) for x in vals)
            #Print the result needed for part 1 if I have it
            if vl==17 and vh==61:
                print "hi, I'm cobot #%s.  I have values %d and %d"%(num,vl,vh)
            lo.send(dict(val=str(vl)))
            hi.send(dict(val=str(vh)))
            vals=[]

def makebot(botdict, num):
    botdict[num].send(dict(num=num))
    return botdict[num]
    
def initialize_cobots(instruction_set, sink):
    bots = defaultdict(cobot)
    outputs = defaultdict(output)
    op_to_track = ['0','1','2']
    for line in instruction_set:
        l = line.split()
        if l[0]=='bot':
            _,n,_,_,_,bol,nl,_,_,_,boh,nh = l
            bot_n = makebot(bots, n)
            lo = makebot(bots, nl) if bol == 'bot' else makebot(outputs, nl)
            hi = makebot(bots, nh) if boh == 'bot' else makebot(outputs, nh)
            bot_n.send(dict(hi=hi, lo=lo))            
        else:
            n = l[-1]
            val = l[1]
            bot_n = makebot(bots, n)
            bot_n.send(dict(val=val))            
    for op in op_to_track:
        outputs[op].send(dict(target=sink))

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
    initialize_cobots(l,s)
