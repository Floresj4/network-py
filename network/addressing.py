import math, operator, re

from math import floor

class Addressing(object):

    def addressToBinary(self, addr):
        #handle the values as integers
        blocks = [int(x) for x in addr.split('.')]

        position = 0
        for block in blocks:
            bits = self.blockToBits(block)
            blocks[position] = bits
            position += 1

        return blocks

    def addressToBinaryStr(self, addr):
        #ha... I could so I did
        return re.sub(r'[\[\]]', '', 
            '.'.join(re.sub(', ', '', str(block)) 
                for block in self.addressToBinary(addr)))

    def bitsToDecimal(self, bits):
        if bits == []:
            return 0
        elif len(bits) != 8:
            raise Exception("8 bits are required to produce a proper octet.")

        decimal = 0
        for i in range(0, 7):
            if bits[i] == '1' or bits[i] == 1:
                decimal += int(math.pow(2, abs(7 - i)))
        
        return decimal

    def blockToBits(self, block):
        bits = []
        #iterate the 8-bit range and reduce the block
        for power in range(7, -1, -1):
            block_value = math.pow(2, power)

            if (block_value <= block):
                bits.append(1)
                block -= block_value
            else: bits.append(0)

        return bits

    def blockToBitsStr(self, block):
        return ''.join(str(b) for b in self.blockToBits(block))

    def addressClass(self, addr):
        '''
        ' A, B, and C are reserved for unicast communication, 1 host to another
        ' D and C do not define the separation of host and network and are reserved 
        ' for multicast, 1 host communicating to a group; streaming video, etc...
        '''
        ntw_bits = self.blockToBitsStr(int(addr.split('.')[0]))

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
    def expandCIDRRange(self, notation):
        tmp = notation.split('/')

        if(len(tmp) is not 2):
            raise('Ensure your cidr is in the form a.b.c.d/n')

        ip = tmp[0]     #ipv4 address
        #validate and translate, the number of shared initial bits
        subnet = self.__validate(ip, tmp[1])

        #things to remember
        #total hosts - 2^n - 2, two addresses reserved (first and last)
        #for the network and broadcast ID 

        print('subnet: ' + str(subnet))

        #account for array offset; -1
        octet_start = floor(subnet / 8)
        print('octet start: ' + str(octet_start))

        masked_bits = subnet - (8 * (octet_start))
        print('masked bits: ' + str(masked_bits))

        net_start = []
        net_end = []
        subnet_mask = []
        range_started = False

        for i, curr_bits in enumerate(self.addressToBinary(tmp[0])):
            if i != octet_start:
                if not range_started:
                    address = self.bitsToDecimal(curr_bits)
                    net_start.append(address)
                    subnet_mask.append(255)
                    net_end.append(address)
                else:
                    net_start.append(255)
                    net_end.append(255)
            else:
                range_started = True
                address = qckmafs(8 - masked_bits - 1)
                net_start.append(address)
                net_end.append(255)

        print('network start: ' + '.'.join(str(s) for s in net_start))
        print('network end: ' + '.'.join(str(e) for e in net_end))
        print('subnet mask: ' + '.'.join(str(m) for m in subnet_mask))

        return {
            'significant_bits': ip,
            'network_prefix': subnet,
            'address_class': self.addressClass(ip),
            'address_bits': self.addressToBinaryStr(ip),
            'network_start': ''.join(str(b) for b in net_start)
        }

    '''
    validate the ip address and subnet values
    and raise exceptions accordingly
    '''
    def __validate(self, ip, subnet):
        try:
            subnet = int(subnet)
            if subnet < 0 or subnet > 32:
                raise Exception('The network prefix must be a valid integer between 0 and 32')
            
            return subnet
        except:
            raise Exception('{} {}'.format('An error occured managing the network prefix.'
                , 'Ensure your cidr is in the form a.b.c.d/n'))

'''
base 2 exponential factorial; did I just make
that up?!  Outside addressing class to be
independently testable
'''
def qckmafs(start):
    if start > 0:
        out = math.pow(2, start) + qckmafs(start - 1)
    else: return math.pow(2, start)
    return out