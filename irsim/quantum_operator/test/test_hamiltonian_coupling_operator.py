import unittest

import numpy as np
import os
import pickle
import sys
ROOTPATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', '..')
sys.path.append(ROOTPATH)
from irsim.core import (
        Bases,
        )
from irsim.quantum_basis import (
        InfraredKet,
        create_ir_ket_filter,
        JahnTellerKet,
        )
from irsim.quantum_operator import (
        PositionalOperator,
        QuadraticOperator,
        HamiltonianCouplingOperator,
        )
from irsim.debug import get_integer_digit


class TestHamiltonianCouplingOperator(unittest.TestCase):
    '''test class of hamiltonian_coupling_operator.py'''

    def setUp(self):
        ## IR bases
        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('<=', 2)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation t1u(4) bases
        self.t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit = 2))

        ## JT bases
        # valid Alpha-J-P combinations which are taken into account
        cmbs = {(1,1,1), (1,2,-1)} # {(Alpha, J, P), (Alpha, J, P)}

        # set Alpha-J-P combinations
        JahnTellerKet.set_alpha_j_p_combinations(cmbs)

        # instantiation jt bases
        self.jt = Bases(JahnTellerKet())

        ## product bases
        self.bases = Bases(self.t1u_4, self.jt)

    def test_calculation(self):
        # ket
        ket0 = self.bases[0] # |t1u(4)_x> == 0
        ket1 = self.bases[1] # |t1u(4)_x> == 1
        ket2 = self.bases[72] # |t1u(4)_x> == 2

        from copy import deepcopy
        initket0 = deepcopy(ket0)
        initket1 = deepcopy(ket1)
        initket2 = deepcopy(ket2)

        # define IR frequency dictionary
        DIC_IR_FREQ = {
                ('t1u', 4): 0.00629777152672,
                }

        # set IR frequency data to PositionalOperator class
        PositionalOperator.set_ir_frequency(DIC_IR_FREQ)

        # positional operator
        q = PositionalOperator('t1u', 4)

        # define quadratic matrix dictionary
        from irsim.database import DIC_QUADRATIC_MATRIX as DIC_Q_MTRX

        # set quadratic matrix data to QuadraticOperator class
        QuadraticOperator.set_quadratic_matrix(DIC_Q_MTRX)

        # set IR filter
        filterFunc = create_ir_ket_filter('<=', 2)
        QuadraticOperator.set_filter('IR', filterFunc)

        # quadratic operator
        Q = QuadraticOperator(q, ('hg', 't1', 't1', 1), q)
        #Q = QuadraticOperator(q, ('hg', 't1', 't1', 1), q, 'theta')

        # set coupling constant dictionary to HamiltonianCoupling class
        DIC_COUP_CONST = {
                (('t1u', 4), ('t1u', 4), 1): -0.000000713859624,
            }
        HamiltonianCouplingOperator.set_coupling_constant(DIC_COUP_CONST)

        # set coupling constant dictionary
        from irsim.database.COUPLING_MATRIX import DIC_COUPLING_MATRIX as DIC_COUP_MTRX
        HamiltonianCouplingOperator.set_coupling_matrix(DIC_COUP_MTRX)

        # set reduced matrix element dictionary
        from irsim.database import DIC_REDUCED_MATRIX_ELEMENT as DIC_RME
        HamiltonianCouplingOperator.set_reduced_matrix_element(DIC_RME)
        #print(HamiltonianCoupling.DIC_MATRIX_RME)

        h_coup = HamiltonianCouplingOperator(Q)

        # constant
        OMEGA = DIC_IR_FREQ[('t1u', 4)]
        W = DIC_COUP_CONST[(('t1u', 4), ('t1u', 4), 1)]
        XI = DIC_RME[((1,1,1),(1,2,-1))]
        CONST = (1/2) * (np.sqrt(q.HBAR/(2 * OMEGA)))**2 * W * XI

        # h_coup|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=-1, P=+1)>
        h_1coup_ket0 = sorted(h_coup(ket0), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in h_1coup_ket0]
        ans = [
            (0, 0, 2, (1, 2, 0, -1)),
            (0, 1, 1, (1, 2, -2, -1)),
            (0, 1, 1, (1, 2, -1, -1)),
            (0, 2, 0, (1, 2, 0, -1)),
            (1, 0, 1, (1, 2, 2, -1)),
            (1, 1, 0, (1, 2, 1, -1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in h_1coup_ket0]
        ans = [
                +2/np.sqrt(3) * CONST * 0.547722557505166,
                +np.sqrt(2) * CONST * (-0.547722557505166),
                +np.sqrt(2) * CONST * (-0.316227766016838),
                -2 * CONST * 0.316227766016838,
                +np.sqrt(2) * CONST * (0.316227766016838),
                +np.sqrt(2) * CONST * (-0.316227766016838),
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # cache check
        # h_coup|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=0, P=+1)>
        ket1.weight = 0.5
        h_1coup_ket1 = sorted(h_coup(ket1), key=lambda ket: ket.qval)
        # h_coup|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=-1, P=+1)>
        h_1coup_ket0 = sorted(h_coup(ket0), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in h_1coup_ket0]
        ans = [
            (0, 0, 2, (1, 2, 0, -1)),
            (0, 1, 1, (1, 2, -2, -1)),
            (0, 1, 1, (1, 2, -1, -1)),
            (0, 2, 0, (1, 2, 0, -1)),
            (1, 0, 1, (1, 2, 2, -1)),
            (1, 1, 0, (1, 2, 1, -1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in h_1coup_ket0]
        ans = [
                +2/np.sqrt(3) * CONST * 0.547722557505166,
                +np.sqrt(2) * CONST * (-0.547722557505166),
                +np.sqrt(2) * CONST * (-0.316227766016838),
                -2 * CONST * 0.316227766016838,
                +np.sqrt(2) * CONST * (0.316227766016838),
                +np.sqrt(2) * CONST * (-0.316227766016838),
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))
        ket1.weight = 1

        # check destroy
        self.assertEqual(ket0.qval, initket0.qval)
        self.assertEqual(ket0.weight, initket0.weight)
        self.assertEqual(ket1.qval, initket1.qval)
        self.assertEqual(ket1.weight, initket1.weight)
        self.assertEqual(ket2.qval, initket2.qval)
        self.assertEqual(ket2.weight, initket2.weight)

if __name__ == '__main__':
    unittest.main()
