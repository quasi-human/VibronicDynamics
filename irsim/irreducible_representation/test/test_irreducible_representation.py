import unittest

import itertools
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
        CreationOperator,
        AnnihilationOperator,
        PositionalOperator,
        QuadraticOperator,
        JahnTellerTransitOperator,
        HamiltonianCouplingOperator,
        )
from irsim.irreducible_representation import (
        IRstate,
        JTstate,
        IrreducibleRepresentation
        )


class TestIrreducibleRepresentation(unittest.TestCase):
    '''test class of irreducible_representation.py'''

    def setUp(self):
        ## IR bases
        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('<=', 1)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation t1u(4) bases
        t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit = 2))
        gu_5 = Bases(*InfraredKet('gu', 5, excitation_limit = 2))
        hu_6 = Bases(*InfraredKet('hu', 6, excitation_limit = 2))

        ## JT bases
        # valid Alpha-J-P combinations which are taken into account
        from irsim.database import DIC_REDUCED_MATRIX_ELEMENT as DIC_RME
        from itertools import chain
        #cmbs = set(chain(*DIC_RME))
        cmbs = {(1,1,1), (1,2,-1)} # {(Alpha, J, P), (Alpha, J, P)}

        # set Alpha-J-P combinations
        JahnTellerKet.set_alpha_j_p_combinations(cmbs)

        # instantiation jt bases
        jt = Bases(JahnTellerKet())

        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('==', 1)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        ## product bases
        self.bases = Bases(t1u_4, gu_5, hu_6, jt)

        # import PSI dictionary
        from irsim.database import DIC_PSI
        self.DIC_PSI = DIC_PSI

        # set PSI dictionary
        IrreducibleRepresentation.set_psi(self.DIC_PSI)

    def test_orthonormality(self):
        for k1, v1 in self.DIC_PSI.items():
            for k2, v2 in self.DIC_PSI.items():
                tot = 0 # innerdot value (should be 0 <= tot <= 1)
                for e1, e2 in itertools.product(v1, v2):
                    if (k1.Gamma1 == k2.Gamma1
                            and k1.Gamma2 == k2.Gamma2
                            and e1.gamma1 == e2.gamma1
                            and e1.gamma2 == e2.gamma2):
                        tot += e1.coef * e2.coef
                # elements: (Gamma1, Gamma2, n, Gamma, gamma)
                if k1 == k2: # should be 1
                    self.assertAlmostEqual(tot, 1, delta=1e-15)
                else: # should be 0
                    self.assertAlmostEqual(tot, 0, delta=1e-15)

    def test_unitary_1(self):
        '''Gamma1 = T1, Gamma2 = T1, nG = 1 t1'''

        jt = JTstate(Alpha=1, J=1, P=1)
        ir = IRstate(mode='t1u', modeNum=4, ex=1)

        # instantiate
        pi = IrreducibleRepresentation(jt, ir, 1, 't1')

        # create matrix operator
        mtrx = pi.create_matrix_operator(self.bases)

        # square matrix
        sq_mtrx = mtrx.dot(mtrx)

        # mtrx * mtrx must be equal to mtrx
        np.testing.assert_allclose(mtrx, sq_mtrx, atol=1e-15)

    def test_unitary_all(self):
        # Possible JT state
        JT_T1 = JTstate(1, 1, 1)
        JT_H = JTstate(1, 2, -1)

        # Possible IR state
        IR_T1  = IRstate('t1u', 4, 1)
        IR_G  = IRstate('gu', 5, 1)
        IR_H  = IRstate('hu', 6, 1)

        # Check all the combinations
        for n, orb in itertools.product((1, 2), ('a', 't1', 't2', 'g', 'h')):
            for jt in (JT_T1, JT_H):
                for ir in (IR_T1, IR_G, IR_H):
                    pi = IrreducibleRepresentation(jt, ir, n, orb)
                    try:
                        mtrx = pi.create_matrix_operator(self.bases)

                    except KeyError:
                        continue

                    # square matrix
                    sq_mtrx = mtrx.dot(mtrx)

                    # mtrx * mtrx must be equal to mtrx
                    np.testing.assert_allclose( mtrx, sq_mtrx, atol=1e-15)

if __name__ == '__main__':
    unittest.main()
