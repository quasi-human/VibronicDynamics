import unittest

class TestJahnTellerKet(unittest.TestCase):
    '''test class of ir_ket.py'''

    def setUp(self):
        import itertools

        import os
        import sys
        sys.path.append(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
        from irsim.core import Bases
        from irsim.quantum_basis import JahnTellerKet

        from collections import namedtuple
        self.JTstate = namedtuple('JTstate', 'Alpha, J, M, P')

        # extract valid Alpha-J-P combinations
        cmbs = {(1,1,1), (1,2,-1)} # (Alpha, J, P)
        #from irsim.database.CONSTANT import DIC_RME
        #cmbs = set(itertools.chain(*DIC_RME))

        # set Alpha-J-P combinations
        JahnTellerKet.set_alpha_j_p_combinations(cmbs)

        # instantiation jt bases
        self.jt = Bases(JahnTellerKet())

    def test_keys(self):
        assert self.jt.keys == [('JT',)]

    def test_hash_index(self):

        jtstate = self.JTstate(Alpha=1, J=1, M=-1, P=+1)
        assert self.jt.dicIndex[(jtstate,)] == 0 # (Alpha, J, M, P)

        jtstate = self.JTstate(Alpha=1, J=1, M=0, P=+1)
        assert self.jt.dicIndex[(jtstate,)] == 1

        jtstate = self.JTstate(Alpha=1, J=2, M=1, P=-1)
        assert self.jt.dicIndex[(jtstate,)] == 6

        jtstate = self.JTstate(Alpha=1, J=2, M=2, P=-1)
        assert self.jt.dicIndex[(jtstate,)] == 7


if __name__ == '__main__':
    unittest.main()
