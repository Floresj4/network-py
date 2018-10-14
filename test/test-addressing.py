import sys
import unittest

sys.path.append('../')

from network.addressing import addressToBinary
from network.addressing import addressClass
from network.addressing import addressToBinaryStr

class TestIpAddressing(unittest.TestCase):
    def Setup(self):
        pass

    def testipaddress(self):
        test_addr = '192.168.23.2'

        self.assertEqual('192.168.23.2', test_addr)
        self.assertEqual('11000000.10101000.00010111.00000010', addressToBinaryStr(test_addr))
        self.assertEqual('C', addressClass(test_addr))

        '''
        private IP address space
        A: 10.0.0.0     10.255.255.255
        B: 172.16.0.0   172.16.31.255
        C: 192.168.0.0  192.168.255.255
        '''

if __name__ == '__main__':
    unittest.main()