import string

def decompress(s):
    pos = 0
    while True:
        if pos >= len(s):
            raise StopIteration
        if s[pos] != '(':
            ss = s[pos]
            pos +=1
            if ss not in string.whitespace:
                yield ss
        elif s[pos]=='(':
            tag = s[pos:s[pos:].find(')')+1+pos]
            chrs,repeat = tag[1:-1].split('x')
            pos+=len(tag)
            ss = s[pos:pos+int(chrs)]*int(repeat)
            pos += int(chrs)
            yield ss

def decompressv2_sum(s):
    pos=0
    while True:
        if pos >= len(s):
            raise StopIteration
        if s[pos] != '(':
            ss = s[pos]
            pos += 1
            if ss not in string.whitespace:
                yield 1
        else:
            tag = s[pos:s[pos:].find(')')+pos+1]
            chrs,repeat = tag[1:-1].split('x')
            pos += len(tag)
            yield  sum(x for x in decompressv2_sum(s[pos:pos+int(chrs)]))*int(repeat)
            pos += int(chrs)
            
if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as thefile:
        newstr = ''
        l = thefile.readlines()
        mysum = 0
        for line in l:
            newstr+= ''.join([x for x in decompress(line)])
            mysum += sum(x for x in decompressv2_sum(line))
    print "total length ",len(newstr)
    print 'total sum', mysum
