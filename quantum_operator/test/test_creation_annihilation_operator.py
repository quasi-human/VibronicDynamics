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
        )


class TestCreationAnnihilationOperator(unittest.TestCase):
    '''test class of creation_annihilation_operator.py'''

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
        ket0 = self.bases[0] # |t1u(4)_x> = 0
        ket1 = self.bases[48] # |t1u(4)_x> = 1
        ket2 = self.bases[72] # |t1u(4)_x> = 2

        from copy import deepcopy
        initket0 = deepcopy(ket0)
        initket1 = deepcopy(ket1)
        initket2 = deepcopy(ket2)

        # opearator
        cre = CreationOperator('t1u', 4, 'x')
        ann = AnnihilationOperator('t1u', 4, 'x')

        # simple creation (init IR level: |0>)
        cre_ket0 = list(cre(ket0))[0]
        assert cre_ket0.qval == (1, 0, 0, (1, 1, -1, 1))
        assert cre_ket0.weight == 1

        # simple annihilation (init IR level: |1>)
        ann_ket1 = list(ann(ket1))[0]
        assert ann_ket1.qval == (0, 0, 0, (1, 1, -1, 1))
        assert ann_ket1.weight == 1

        # creation -> annihilation (init IR level: |0>)
        ann_cre_ket0 = list((ann * cre)(ket0))[0]
        assert ann_cre_ket0.qval == (0, 0, 0, (1, 1, -1, 1))
        assert ann_cre_ket0.weight == 1

        # annihilation -> creation (init IR level: |1>)
        cre_ann_ket1 = list((cre * ann)(ket1))[0]
        assert cre_ann_ket1.qval == (1, 0, 0, (1, 1, -1, 1))
        self.assertAlmostEqual(cre_ann_ket1.weight, 1, delta=1e-15)

        # creation -> annihilation (init IR level: |1>)
        ann_cre_ket1 = list((ann * cre)(ket1))[0]
        assert ann_cre_ket1.qval == (1, 0, 0, (1, 1, -1, 1))
        self.assertAlmostEqual(ann_cre_ket1.weight, 2, delta=1e-15)

        # simple creation (init IR level: |2>)
        cre_ket2 = list(cre(ket2))[0]
        assert cre_ket2.qval == (3, 0, 0, (1, 1, -1, 1))
        self.assertAlmostEqual(cre_ket2.weight, np.sqrt(3), delta=1e-15)

        # simple annihilation (init IR level: |2>)
        ann_ket2 = list(ann(ket2))[0]
        assert ann_ket2.qval == (1, 0, 0, (1, 1, -1, 1))
        self.assertAlmostEqual(ann_ket2.weight, np.sqrt(2), delta=1e-15)

        # over creation (init IR level: |2>)
        cre_cre_ket2 = list((cre * cre)(ket2)) # over intermediate limit
        assert cre_cre_ket2 == []

        # over annihilation (init IR level: |0>)
        ann_ket0 = list(ann(ket0)) # less than vacuum level
        assert ann_ket0 == []

        # check destroy
        self.assertEqual(ket0.qval, initket0.qval)
        self.assertEqual(ket0.weight, initket0.weight)
        self.assertEqual(ket1.qval, initket1.qval)
        self.assertEqual(ket1.weight, initket1.weight)
        self.assertEqual(ket2.qval, initket2.qval)
        self.assertEqual(ket2.weight, initket2.weight)


if __name__ == '__main__':
    unittest.main()
