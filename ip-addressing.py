import math

ipaddress = '192.168.23.2'

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
    return ''.join(addressToBinary(addr))

def blockToBits(block):
    bits = []

    for power in range(7, -1, -1):
        block_value = math.pow(2, power)

        if (block_value <= block):
            bits.append(1)
            block -= block_value
        else: bits.append(0)

    return bits

def blockToBitsStr(block):
    return ''.join(str(b) for b in blockToBits(block))

print(addressToBinary(ipaddress))
print(blockToBitsStr(255))