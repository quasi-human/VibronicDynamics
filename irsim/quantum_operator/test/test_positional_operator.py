import unittest

import numpy as np
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
        CreationOperator,
        AnnihilationOperator,
        PositionalOperator,
        )
from irsim.debug import get_integer_digit


class TestPositionalOperator(unittest.TestCase):
    '''test class of positional_operator.py'''

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

        # creation annihilation opearator
        cre = CreationOperator('t1u', 4, 'x')
        ann = AnnihilationOperator('t1u', 4, 'x')

        # define IR frequency dictionary
        DIC_IR_FREQ = {
                ('t1u', 4): 0.00629777152672,
                }

        # set IR frequency data to PositionalOperator class
        PositionalOperator.set_ir_frequency(DIC_IR_FREQ)

        # positional operator
        q = PositionalOperator('t1u', 4, 'x')

        # constant
        OMEGA = DIC_IR_FREQ[('t1u', 4)]
        CONST = np.sqrt(q.HBAR/(2 * OMEGA))
       
        # q|IR=0>
        q_ket0 = list(q(ket0))[0]
        assert q_ket0.qval == (1, 0, 0, (1, 1, -1, 1))
        self.assertAlmostEqual(q_ket0.weight, CONST, delta=1e-15)

        # q|IR=1>
        q_ket1 = sorted(q(ket1), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in q_ket1]
        ans = [
            (0, 0, 0, (1, 1, -1, 1)),
            (2, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in q_ket1]
        ans = [
                CONST * 1,
                CONST * np.sqrt(2),
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # q|IR=2>
        q_ket2 = sorted(q(ket2), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in q_ket2]
        ans = [
            (1, 0, 0, (1, 1, -1, 1)),
            (3, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in q_ket2]
        ans = [
                CONST * np.sqrt(2),
                CONST * np.sqrt(3),
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # q|IR=3>
        q_ket3 = sorted((q*cre)(ket2), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in q_ket3]
        ans = [
            (2, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in q_ket3]
        ans = [
                CONST * np.sqrt(3) * np.sqrt(3),
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
