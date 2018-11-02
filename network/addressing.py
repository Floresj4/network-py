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

        start = floor(subnet / 8)
        abits = []  #use the address to get bits for mask
        for i, b in enumerate(self.addressToBinary(tmp[0])):
            for j in range(0, len(b)):
                bit_pos = (8 * i + j)
            abits += b

        return {
            'significant_bits': ip,
            'network_prefix': subnet,
            'address_class': self.addressClass(ip),
            'address_bits': self.addressToBinaryStr(ip),
            'abits': ''.join(str(b) for b in abits)
        }

    def __validate(self, ip, subnet):
        try:
            subnet = int(subnet)
            if subnet < 0 or subnet > 32:
                raise Exception('The network prefix must be a valid integer between 0 and 32')
            
            return subnet
        except:
            raise Exception('{} {}'.format('An error occured managing the network prefix.'
                , 'Ensure your cidr is in the form a.b.c.d/n'))
