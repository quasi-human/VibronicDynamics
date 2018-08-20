import unittest

import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
from irsim.core import (
        Bases,
        )
from irsim.quantum_basis import (
        InfraredKet,
        create_ir_ket_filter,
        JahnTellerKet,
        )
from irsim.quantum_operator import (
        JahnTellerTransitOperator,
        )
from irsim.debug import get_integer_digit


class TestJahnTellerTransitOperator(unittest.TestCase):
    '''test class of jahn_teller_transit_operator.py'''

    def setUp(self):
        ## IR bases
        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('<=', 2)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation t1u(4) bases
        self.t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit=2))

        ## JT bases
        # define valid Alpha-J-P combinations
        cmbs = {(1,1,1), (1,2,-1)} # (Alpha, J, P)

        # set Alpha-J-P combinations
        JahnTellerKet.set_alpha_j_p_combinations(cmbs)

        # instantiation jt bases
        self.jt = Bases(JahnTellerKet())

        ## product bases
        self.bases = Bases(self.t1u_4, self.jt)

    def test_calculation(self):
        # ket
        ket0 = self.bases[0] # |t1u(4)_x> == 0
        ket1 = self.bases[48] # |t1u(4)_x> == 1
        ket2 = self.bases[72] # |t1u(4)_x> == 2

        from copy import deepcopy
        initket0 = deepcopy(ket0)
        initket1 = deepcopy(ket1)
        initket2 = deepcopy(ket2)

        # jahn-teller transit operator
        jtt = JahnTellerTransitOperator(toAlpha=1, toJ=2, toM=-1, toP=-1)

        # jtt|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=-1, P=+1)>
        jtt_ket0 = sorted(jtt(ket0), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in jtt_ket0]
        ans = [
            (0, 0, 0, (1, 2, -1, -1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in jtt_ket0]
        ans = [
                1,
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # check destroy
        self.assertEqual(ket0.qval, initket0.qval)
        self.assertEqual(ket0.weight, initket0.weight)
        self.assertEqual(ket1.qval, initket1.qval)
        self.assertEqual(ket1.weight, initket1.weight)
        self.assertEqual(ket2.qval, initket2.qval)
        self.assertEqual(ket2.weight, initket2.weight)


if __name__ == '__main__':
    unittest.main()
