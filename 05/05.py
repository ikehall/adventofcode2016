import hashlib
import itertools

poss = '01234567'

def char_from_hash(hashstr):
    leading_digit, repeat = [(k, len(list(g)))
                             for k,g in itertools.groupby(hashstr)][0]
    if leading_digit != '0' or repeat < 5:
        return ''
    return hashstr[5]

def char2_from_hash(hashstr):
    if hashstr[5] not in poss:
        return None, None
    leading_digit, repeat = [(k, len(list(g)))
                             for k,g in itertools.groupby(hashstr)][0]
    if leading_digit != '0' or repeat < 5:
        return None, None
    return int(hashstr[5]), hashstr[6]
    
def hash_id_plus_index(strng, index):
    return hashlib.md5(strng+str(index)).hexdigest()

    
def find_password(doorid, start_index=0):
    code = char_from_hash(hash_id_plus_index(doorid, start_index))
    while len(code) < 8:
        if start_index%1000000==0:
            print code, start_index
        start_index += 1
        code += char_from_hash(hash_id_plus_index(doorid, start_index))
    return code

def find_password2(doorid, start_index=0):
    code = ['-']*8
    while '-' in code:
        if start_index%1000000==0:
            print code, start_index
        start_index += 1
        pos, char = char2_from_hash(hash_id_plus_index(doorid, start_index))
        if pos is not None and code[pos]=='-':
            code[pos] = char
    return ''.join(code)


if __name__ == '__main__':
    import sys
    print find_password2(sys.argv[1])
