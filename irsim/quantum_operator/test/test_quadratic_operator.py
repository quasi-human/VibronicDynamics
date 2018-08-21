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
        QuadraticOperator,
        )
from irsim.debug import get_integer_digit


class TestQuadraticOperator(unittest.TestCase):
    '''test class of quadratic_operator.py'''

    def setUp(self):
        ## IR bases
        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('<=', 2)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation t1u(4) bases
        self.t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit = 2))

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
        #q = PositionalOperator('t1u', 4, 'x')
        q = PositionalOperator('t1u', 4)

        # define IR frequency dictionary
        DIC_Q_MTRX = {
                ('hg', 't1', 't1', 1, 'theta'):
                    np.sqrt(1/6) * np.array([
                            [ -1,  0,  0],
                            [  0, -1,  0],
                            [  0,  0,  2]]),
                    }

        # set quadratic matrix data to QuadraticOperator class
        QuadraticOperator.set_quadratic_matrix(DIC_Q_MTRX)

        # set IR filter
        filterFunc = create_ir_ket_filter('<=', 2)
        QuadraticOperator.set_filter('IR', filterFunc)

        # quadratic operator
        Q = QuadraticOperator(q, ('hg', 't1', 't1', 1), q, 'theta')

        # constant
        OMEGA = DIC_IR_FREQ[('t1u', 4)]
        CONST = np.sqrt(q.HBAR/(2 * OMEGA))
       
        # Q|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=-1, P=+1)>
        Q_ket0 = sorted(Q(ket0), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in Q_ket0]
        ans = [
            (0, 0, 2, (1, 1, -1, 1)),
            (0, 2, 0, (1, 1, -1, 1)),
            (2, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in Q_ket0]
        ans = [
                CONST**2 * np.sqrt(2) * np.sqrt(1/6) * 2,
                CONST**2 * np.sqrt(2) * np.sqrt(1/6) * -1,
                CONST**2 * np.sqrt(2) * np.sqrt(1/6) * -1,
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # Q|IR: x=1, y=0, z=0, JT: (Alpha=1, J=1, M=-1, P=+1)>
        Q_ket1 = sorted(Q(ket1), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in Q_ket1]
        ans = [
            (1, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in Q_ket1]
        ans = [
                - np.sqrt(6) * (1/3) * CONST**2,
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
