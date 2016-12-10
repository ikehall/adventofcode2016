from operator import mul

class Bot(object):
    def __init__(self, num, botnet, instructions=None, vals=None):
        self.vals = sorted(vals) if vals is not None else []
        self.num = num
        self.high, self.low = self.process_instructions(instructions)
        self.botnet = botnet
        
    def process_instructions(self, instructions):
        low = instructions.split()[5:7]
        hi = instructions.split()[-2:]
        return hi, low
        
    def can_move(self):
        return len(self.vals)==2

    def move(self):
        v1,v2 = sorted(int(x) for x in self.vals)
        if v1==17 and v2==61:
            print "hi, I'm bot %s, and I have microchips 17 and 61"%self.num
        self.vals=[]
        self.botnet.give(str(v1), str(v2), self.low, self.high)
        
    def receive(self, num):
        self.vals.append(num)
        if self.can_move():
            self.move()

class Output(object):
    def __init__(self, num):
        self.vals = []
        self.num = num

    def receive(self, num):
        self.vals.append(num)

class Botnet(object):
    def __init__(self, instruction_set):
        self.bots = self.init_bots(instruction_set)
        self.outputs = self.init_outputs(instruction_set)

    def init_outputs(self, insts):
        output_nums = []
        for line in insts:
            words = line.split()
            if words[5]=='output':
                output_nums.append(words[6])
            if words[-2]=='output':
                output_nums.append(words[-1])
        theoutputs = {num:Output(num) for num in output_nums}
        return theoutputs
        
    def init_bots(self, insts):
        bot_nums = []
        start = {}
        instructions = {}
        for line in insts:
            words = line.split()
            if words[0] == 'value':
                val = words[1]
                bot = words[-1]
                if bot not in bot_nums:
                    bot_nums.append(bot)
                if bot in start:
                    start[bot].append(val)
                else:
                    start[bot]=[val]
                    
            if words[0] == 'bot':
                bot = words[1]
                inst = line
                if bot not in bot_nums:
                    bot_nums.append(bot)
                instructions[bot]=inst
                if words[5] == 'bot':
                    bot_nums.append(words[6])
                if words[-2] == 'bot':
                    bot_nums.append(words[-1])
                
        thebots = {num:Bot(num, self,
                           instructions=instructions.get(num),
                           vals=start.get(num)) for num in bot_nums}
        return thebots
        
    def give(self, numlo, numhi, dest_lo, dest_hi):
        self._give(numlo, dest_lo)
        self._give(numhi, dest_hi)

    def _give(self, num, dest):
        if dest[0]=='output':
            self.outputs[dest[1]].receive(num)
        elif dest[0]=='bot':
            self.bots[dest[1]].receive(num)


    def run(self):
        while True:
            moves = 0
            for _, bot in self.bots.iteritems():
                if bot.can_move():
                    bot.move()
                    moves += 1
            if moves == 0:
                keys = ('0','1','2')
                ops = [sum([int(x) for x in self.outputs[y].vals]) for y in keys]
                print reduce(mul, ops)
                return


#####FOR FUN LATER#####
#do this in coroutines!#

    
if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        l = thefile.readlines()
    bn = Botnet(l)
    bn.run()
    
    
    
