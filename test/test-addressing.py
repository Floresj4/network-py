import sys
import unittest
import json

sys.path.append('../')

from network.addressing import Addressing

class TestIpAddressing(unittest.TestCase):
    def Setup(self):
        pass

    def test_ip_address(self):
        test_addr = '192.168.23.2'

        addressing = Addressing()
        self.assertEqual('192.168.23.2', test_addr)
        self.assertEqual('11000000.10101000.00010111.00000010', addressing.addressToBinaryStr(test_addr))
        self.assertEqual('C', addressing.addressClass(test_addr))

        '''
        private IP address space
        A: 10.0.0.0     10.255.255.255
        B: 172.16.0.0   172.16.31.255
        C: 192.168.0.0  192.168.255.255
        '''

    def test_cidr_notation(self):
        addressing = Addressing()

        #assert some error scenarios
        with(self.assertRaises(Exception)):
            addressing.expandCIDRRange('1.2.3.4/')

        with(self.assertRaises(Exception)):
            addressing.expandCIDRRange('1.2.3.4/-1')

        with(self.assertRaises(Exception)):
            addressing.expandCIDRRange('1.2.3.4/33')

        test_notation = '192.168.0.0/22'
        print('test_cidr_notation: {}'.format(test_notation))
        print(json.dumps(
            addressing.expandCIDRRange(test_notation),
            indent = 4))

if __name__ == '__main__':
    unittest.main()