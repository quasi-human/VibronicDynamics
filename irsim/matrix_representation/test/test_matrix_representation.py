import unittest

import numpy as np
import os
import pickle
import sys
from time import time
ROOTPATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', '..')
sys.path.append(ROOTPATH)
from irsim.core import (
        Bases,
        )
from irsim.quantum_basis import (
        create_ir_ket_filter,
        InfraredKet,
        JahnTellerKet,
        )
from irsim.quantum_operator import (
        PositionalOperator as q,
        QuadraticOperator as Q,
        HamiltonianCouplingOperator as H_coupling,
        HamiltonianInfraredOperator as H_IR,
        HamiltonianJahnTellerOperator as H_JT,
        )
from irsim.matrix_representation import (
        op2mtrx,
        diagonalize_helmitian_operator,
        )
from irsim.debug.helper import get_integer_digit


class TestMatrixRepresentation(unittest.TestCase):
    '''test matrix_representation.py'''

    def setUp(self):
        ### BASES
        ## IR bases
        IR_LIMIT = 0
        # impose excitation limit to IR bases
        filterFunc = create_ir_ket_filter('<=', IR_LIMIT)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation ir bases
        t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit = IR_LIMIT))
        gu_5 = Bases(*InfraredKet('gu', 5, excitation_limit = IR_LIMIT))
        hu_6 = Bases(*InfraredKet('hu', 6, excitation_limit = IR_LIMIT))


        ## JT bases
        # valid Alpha-J-P combinations which are taken into account
        cmbs = {(1,0,1), (1,2,-1)} # {(Alpha, J, P), (Alpha, J, P)}

        # set Alpha-J-P combinations
        JahnTellerKet.set_alpha_j_p_combinations(cmbs)

        # instantiation jt bases
        jt = Bases(JahnTellerKet())


        ## product bases
        # set filter 
        #filterFunc = create_ir_ket_filter('<=', IR_LIMIT)
        filterFunc = create_ir_ket_filter('==', IR_LIMIT)
        Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

        # instantiation product bases
        #bases = Bases(t1u_4, gu_5, hu_6, jt)
        bases = Bases(t1u_4, jt)



        ### QUANTUM OPERATOR
        ## positional operator
        # fetch IR frequency data
        from irsim.database import DIC_IR_FREQUENCY as DIC_IR_FREQ

        # set IR frequency data to PositionalOperator class
        q.set_ir_frequency(DIC_IR_FREQ)


        ## quadratic operator
        # fetch IR frequency data
        from irsim.database import DIC_QUADRATIC_MATRIX as DIC_Q_MTRX

        # set quadratic matrix data to QuadraticOperator class
        Q.set_quadratic_matrix(DIC_Q_MTRX)

        # set IR filter to class QuadraticOperator
        filterFunc = create_ir_ket_filter('<=', IR_LIMIT)
        Q.set_filter('IR', filterFunc)


        ## hamiltonian coupling operator
        # fetch coupling constant data
        from irsim.database import DIC_COUPLING_CONSTANT as DIC_COUP_CONST

        # set coupling constant data to HamiltonianCouplingOperator
        H_coupling.set_coupling_constant(DIC_COUP_CONST)

        # fetch coupling matrix data
        path = os.path.join(ROOTPATH, 'irsim', 'database', 'HIRmat.pickle')
        with open(path, 'rb') as f:
            DIC_COUP_MTRX = pickle.load(f)

        # set coupling constant dictionary to HamiltonianCouplingOperator
        H_coupling.set_coupling_matrix(DIC_COUP_MTRX)

        # set reduced matrix element dictionary to HamiltonianCouplingOperator
        from irsim.database import DIC_REDUCED_MATRIX_ELEMENT as DIC_RME
        H_coupling.set_reduced_matrix_element(DIC_RME)

        # instantiation
        h_coupling = H_coupling(
                Q(q('t1u',4), ('hg', 't1', 't1', 1), q('t1u',4)),
#                Q(q('gu',5), ('hg', 'g', 'g', 1), q('gu',5)),
#                Q(q('hu',6), ('hg', 'h', 'h', 1), q('hu',6)),
#                Q(q('hu',6), ('hg', 'h', 'h', 2), q('hu',6)),
#                Q(q('t1u',4), ('hg', 't1', 'g', 1), q('gu',5)),
#                Q(q('t1u',4), ('hg', 't1', 'h', 1), q('hu',6)),
#                Q(q('gu',5), ('hg', 'g', 'h', 1), q('hu',6)),
#                Q(q('gu',5), ('hg', 'g', 'h', 2), q('hu',6)),
                )


        ## hamiltonian infrared operator
        # set ir frequency data
        H_IR.set_ir_frequency(DIC_IR_FREQ)

        # instantiation
        h_ir = H_IR()


        ## hamiltonian jahn-teller operator
        # fetch & convert jt eigen energy data to Python dictionary
        #from irsim.database import import_vibronic_energy_levels
        from irsim.database import DIC_VIBRONIC_ENERGY_LEVEL

        # set jt eigen energy data to HamiltonianJahnTellerOperator
        H_JT.set_jt_eigen_energy(DIC_VIBRONIC_ENERGY_LEVEL)

        # instantiation
        h_jt = H_JT()


        #################################
        ## create total Hamiltonian
        H = h_ir + h_jt + h_coupling
        #################################

        self.bases = bases
        self.H = H


    def test_op2mtrx(self):

        ## MATRIX DIAGONALIZATION
        # convert operator to matrix representation
        mtrx = op2mtrx(self.bases, self.H, self.bases)

        # get eigen value (energy) and eigen function
        #eigenEnergy, eigenVector = diagonalize_helmitian_operator(mtrx)

        expected = np.array(
    [[-0.00549454, 0,          0,          0,          0,          0,        ],
     [ 0,         -0.0069113,  0,          0,          0,          0,        ],
     [ 0,          0,         -0.0069113,  0,          0,          0,        ],
     [ 0,          0,          0,         -0.0069113,  0,          0,        ],
     [ 0,          0,          0,          0,         -0.0069113,  0,        ],
     [ 0,          0,          0,          0,          0,         -0.0069113,],
     ])

        np.testing.assert_allclose(mtrx, expected, rtol = 1e-5)

    def test_non_hermitian_diagonalization(self):

        mtrx = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])

        with self.assertRaises(ValueError):
            E, C = diagonalize_helmitian_operator(mtrx)

if __name__ == '__main__':
    unittest.main()
