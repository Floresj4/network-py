import math, operator, re

def addressToBinary(addr):
    #handle the values as integers
    blocks = [int(x) for x in addr.split('.')]

    position = 0
    for block in blocks:
        bits = blockToBits(block)
        blocks[position] = bits
        position += 1

    return blocks

def addressToBinaryStr(addr):
    #ha... I could so I did
    return re.sub(r'[\[\]]', '', 
        '.'.join(re.sub(', ', '', str(block)) 
            for block in addressToBinary(addr)))

def blockToBits(block):
    bits = []
    #iterate the 8-bit range and reduce the block
    for power in range(7, -1, -1):
        block_value = math.pow(2, power)

        if (block_value <= block):
            bits.append(1)
            block -= block_value
        else: bits.append(0)

    return bits

def blockToBitsStr(block):
    return ''.join(str(b) for b in blockToBits(block))

def addressClass(addr):
    '''
    ' A, B, and C are reserved for unicast communication, 1 host to another
    ' D and C do not define the separation of host and network and are reserved 
    ' for multicast, 1 host communicating to a group; streaming video, etc...
    '''
    ntw_bits = blockToBitsStr(int(addr.split('.')[0]))

    #fixed address class to test against
    for c in ['0', '10', '110', '1110', '1111']:
        if(operator.eq(ntw_bits[:len(c)], c)):
            return chr(64 + len(c))

    return '?'