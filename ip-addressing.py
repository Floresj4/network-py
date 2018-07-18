import math

ipaddress = '192.168.23.2'

def addressToBinary(addr):
    #handle the values as integers
    blocks = [int(x) for x in addr.split('.')]

    for dgt in blocks:
        bits = []
        for power in range(7, -1, -1):
            block_value = math.pow(2, power)
            if (block_value <= dgt):
                bits.append(1)
                dgt -= block_value
            else: bits.append(0)
        print(bits)

    return blocks

print(addressToBinary(ipaddress))