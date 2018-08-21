import unittest

from copy import deepcopy
import os
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
        HamiltonianJahnTellerOperator,
        )
from irsim.debug import get_integer_digit


class TestHamiltonianJahnTellerOperator(unittest.TestCase):
    '''test class of hamiltonian_jahn_teller_operator.py'''

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
        ket0 = self.bases[0] # |JT> == (Alpha=1, J=1, P=+1)
        ket1 = self.bases[3] # |JT> == (Alpha=1, J=2, P=-1)
        ket2 = self.bases[64] # |t1u(4)_x> == 1 |t1u(4)_y> == 1

        initket0 = deepcopy(ket0)
        initket1 = deepcopy(ket1)
        initket2 = deepcopy(ket2)

        # convert raw vibronic energy data
        from irsim.database.VIBRONIC_ENERGY_LEVEL import DIC_VIBRONIC_ENERGY_LEVEL
        HamiltonianJahnTellerOperator.set_jt_eigen_energy(DIC_VIBRONIC_ENERGY_LEVEL)
        h_jt = HamiltonianJahnTellerOperator()

        # h_jt|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=1, M=-1, P=+1)>
        h_jt_ket0 = sorted(h_jt(ket0), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in h_jt_ket0]
        ans = [
            (0, 0, 0, (1, 1, -1, 1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in h_jt_ket0]
        ans = [
                h_jt.DIC_JT_EIGEN_ENERGY[(1,1,1)]
                ]
        for w, a in zip(weight, ans):
            dd = get_integer_digit(w)
            self.assertAlmostEqual(w, a, delta=10**(-15+dd))

        # h_jt|IR: x=0, y=0, z=0,  JT: (Alpha=1, J=2, M=-2, P=-1)>
        h_jt_ket1 = sorted(h_jt(ket1), key=lambda ket: ket.qval)
        qval = [ket.qval for ket in h_jt_ket1]
        ans = [
            (0, 0, 0, (1, 2, -2, -1)),
            ]
        self.assertEqual(qval, ans)
        weight = [ket.weight for ket in h_jt_ket1]
        ans = [
                h_jt.DIC_JT_EIGEN_ENERGY[(1,2,-1)]
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
