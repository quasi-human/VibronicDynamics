import unittest

import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
from irsim.core import Bases
from irsim.quantum_basis import InfraredKet, create_ir_ket_filter


class TestInfraredKet(unittest.TestCase):
    '''test class of ir_ket.py'''

    def setUp(self):
        filterFunc = create_ir_ket_filter('<=', 2)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation t1u(4) bases
        self.t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit = 2))

    def test_keys(self):
        assert self.t1u_4.keys == [
                ('IR', 't1u', 4, 'x',),
                ('IR', 't1u', 4, 'y',),
                ('IR', 't1u', 4, 'z',),
                ]

    def test_hash(self):
        assert self.t1u_4.get_index_from_qval((0,0,0)) == 0
        assert self.t1u_4.get_index_from_qval((0,0,1)) == 1
        assert self.t1u_4.get_index_from_qval((1,1,0)) == 8
        assert self.t1u_4.get_index_from_qval((2,0,0)) == 9

    def test_set_over_the_intermediate_limit_value(self):
        '''Raise ValueError if given qval is over the intermediate limit.
        intermediate limit === excitation limit + 1'''

        # check instantiation error
        with self.assertRaises(ValueError):
            t1u_4_x = InfraredKet('t1u', 4, 'x', qval=4, excitation_limit=2)

        # check dynamical set error
        t1u_4_x = InfraredKet('t1u', 4, 'x', qval=0, excitation_limit=2)
        with self.assertRaises(ValueError):
            t1u_4_x.qval = 4



if __name__ == '__main__':
    unittest.main()
