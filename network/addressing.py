import math, operator, re

from math import floor

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

'''
Expand Classless Inter-Domain Routing notation into
a starting and ending IP address.
@param cidr - 192.168.1.1/32
'''
def expandCIDRRange(notation):
    tmp = notation.split('/')

    if(len(tmp) is not 2):
        raise('Ensure your cidr is in the form a.b.c.d/n')

    ip = tmp[0]     #ipv4 address
    network = 0     #prefix length, the number of shared initial bits

    try:
        network = int(tmp[1])
        if network < 0 or network > 32:
            raise Exception('The network prefix must be a valid integer between 0 and 32')
    except:
        raise Exception('{} {}'.format('An error occured managing the network prefix.'
            , 'Ensure your cidr is in the form a.b.c.d/n'))

    #use the address to get bits for mask
    abits = addressToBinary(tmp[0])
    start = floor(network / 8) - 1
    abits = []

    return {
        'significant_bits': ip,
        'network_prefix': network,
        'address_class': addressClass(ip),
        'address_bits': addressToBinaryStr(ip),
        'abits': ''.join(str(b) for b in abits),
        'start': start
    }