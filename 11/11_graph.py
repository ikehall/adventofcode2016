from itertools import chain, combinations, product
#There are 10 items plus one elevator.  Each item can be on one of four floors
#That means that there are 4,194,304 possible configurations.
#Each chip has a corresponding generator.  If a chip is on a floor with
#any generator and also not with it's corresponding generator, it gets fried.

#Use an easy way to identify chips, generators:
#chips will be numbered 1-5
#Generators will have a number of 10x, where x is the number of the chip
#If we had more than 9 chips, go to 100x, etc
#A floor will be represented by an array of numbers
#Elevator will be represented with zero



def is_fried(config):
    for floor in config:
        if any(x>10 for x in floor) and any(10*x not in floor for x in floor if x<10):
            return True
    return False
    
def find_elevator(config):
    for floor, f in enumerate(config):
        if 0 in f:
            return floor
    print config
    raise RuntimeError("elevator has disappeared!")
    
def find_shortest_path(initial_configs, final_config, visited_configs=None, prev_moves=0):
    if visited_configs is None:
        visited_configs = set()
        initial_configs = (initial_configs,)
    print "step %d, nodes visited=%d"%(prev_moves, len(visited_configs))
    configs_for_next_move = set()
    for config in initial_configs:
        efloor = find_elevator(config)
        possible_next_configs = valid_moves(config, efloor, len(config), visited_configs)
        for next_config in possible_next_configs:
            visited_configs.add(next_config)
            configs_for_next_move.add(next_config)
        if final_config in configs_for_next_move:
            return prev_moves + 1
    return find_shortest_path(configs_for_next_move, final_config, visited_configs, prev_moves+1)
            
def valid_moves(config, efloor, numfloors=4, visited_configs=None):
    newfloors = (efloor+n for n in (1,-1) if efloor+n in xrange(numfloors))
    flooritems = set(x for x in config[efloor] if x != 0)
    for items, newfloor in product(chain(combinations(flooritems,2),
                                         combinations(flooritems,1)),
                                   newfloors):
        newconfig = []
        for i,floor in enumerate(config):
            if i != efloor and i!= newfloor:
                newconfig.append(floor)
            elif i == efloor:
                new_floor_config = frozenset(floor.difference(set(items).union([0])))
                newconfig.append(new_floor_config)
            elif i == newfloor:
                new_floor_config = frozenset(floor.union(set(items).union(set([0]))))
                newconfig.append(new_floor_config)
        newconfig = tuple(newconfig)
        if visited_configs is not None and newconfig in visited_configs:
            continue
        if not is_fried(newconfig):
            yield newconfig
            
    
    
    
def initialize(config_text):
    items_in_floor = []
    elements = set()
    all_items = set()
    for floor, line in enumerate(config_text):
        items_in_floor.append(set())
        item_strings = [item.strip(', and').strip().strip('.') for item in line.split(' a ')[1:]]
        for jstr in item_strings:
            items_in_floor[floor].add(jstr)
            elements.add(jstr.split()[0].split('-')[0])
    floor_config = []
    element_nums = {ename:i+1 for i, ename in enumerate(elements)}
    for floor, floorset in enumerate(items_in_floor):
        s = set()
        for item in floorset:
            element_name = item.split()[0].split('-')[0]
            if 'generator' in item:
                itemnum = element_nums[element_name]*10
            else:
                itemnum = element_nums[element_name]
            s.add(itemnum)
            all_items.add(itemnum)
        floor_config.append(frozenset(s))
    #Add the elevator
    print floor_config[0]
    f = set(floor_config[0])
    f.add(0)
    floor_config[0] = frozenset(f)
    final_config = []
    for i in xrange(len(floor_config)):
        if i != len(floor_config)-1:
            final_config.append(frozenset())
        else:
            final_config.append(frozenset(all_items).union(set((0,))))
    return tuple(floor_config), tuple(final_config)
            

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        contents = thefile.readlines()
    init_config, final_config = initialize(contents)
    print find_shortest_path(init_config, final_config)
