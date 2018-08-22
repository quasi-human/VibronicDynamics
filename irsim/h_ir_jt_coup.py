import datetime
import dill
import numpy as np
import os
import sys
ROOTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
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
        is_symmetric,
        is_diagonalized,
        diagonalize_helmitian_operator,
        )
from irsim.file_handler import (
        create_diagonalization_save_directory_name as create_dir_name,
        )

if __name__ == '__main__':
    ### BASES

    ## IR bases
    IR_LIMIT = 1
    INEQUALITY = '<='

    # impose excitation limit to IR bases
    filterFunc = create_ir_ket_filter('<=', IR_LIMIT)
    Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

    # instantiation ir bases
    t1u_4 = Bases(*InfraredKet('t1u', 4, excitation_limit=IR_LIMIT))
    gu_5 = Bases(*InfraredKet('gu', 5, excitation_limit=IR_LIMIT))
    hu_6 = Bases(*InfraredKet('hu', 6, excitation_limit=IR_LIMIT))

    ## JT bases
    # valid Alpha-J-P combinations which are taken into account
    cmbs = {(1,1,1), (1,2,-1)} # {(Alpha, J, P), (Alpha, J, P)}

    # set Alpha-J-P combinations
    JahnTellerKet.set_alpha_j_p_combinations(cmbs)

    # instantiation jt bases
    jt = Bases(JahnTellerKet())


    ## product bases
    # set filter 
    filterFunc = create_ir_ket_filter(INEQUALITY, IR_LIMIT)
    Bases.set_filter('IR', filterFunc) # set IR filter to class Bases

    # instantiation product bases
    bases = Bases(t1u_4, gu_5, hu_6, jt)



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
    filterFunc = create_ir_ket_filter(INEQUALITY, IR_LIMIT)
    Q.set_filter('IR', filterFunc)


    ## hamiltonian coupling operator
    # fetch coupling constant data and set to hamiltonian
    from irsim.database import DIC_COUPLING_CONSTANT as DIC_COUP_CONST
    H_coupling.set_coupling_constant(DIC_COUP_CONST)

    # fetch coupling matrix data and set to hamiltonian
    from irsim.database.COUPLING_MATRIX import DIC_COUPLING_MATRIX as DIC_COUP_MTRX
    H_coupling.set_coupling_matrix(DIC_COUP_MTRX)

    # fetch reduced matrix element data to hamiltonian
    from irsim.database import DIC_REDUCED_MATRIX_ELEMENT as DIC_RME
    H_coupling.set_reduced_matrix_element(DIC_RME)

    # instantiation
    h_coupling = H_coupling(
            Q(q('t1u',4), ('hg', 't1', 't1', 1), q('t1u',4)),
            Q(q('gu',5), ('hg', 'g', 'g', 1), q('gu',5)),
            Q(q('hu',6), ('hg', 'h', 'h', 1), q('hu',6)),
            Q(q('hu',6), ('hg', 'h', 'h', 2), q('hu',6)),
            Q(q('t1u',4), ('hg', 't1', 'g', 1), q('gu',5)),
            Q(q('t1u',4), ('hg', 't1', 'h', 1), q('hu',6)),
            Q(q('gu',5), ('hg', 'g', 'h', 1), q('hu',6)),
            Q(q('gu',5), ('hg', 'g', 'h', 2), q('hu',6)),
            )


    ## hamiltonian infrared operator
    # set ir frequency data
    H_IR.set_ir_frequency(DIC_IR_FREQ)

    # instantiation
    h_ir = H_IR()


    ## hamiltonian jahn-teller operator
    # fetch jt eigen energy data and set to hamiltonian
    from irsim.database.VIBRONIC_ENERGY_LEVEL import DIC_VIBRONIC_ENERGY_LEVEL as DIC_JT_EE
    H_JT.set_jt_eigen_energy(DIC_JT_EE)

    # instantiation
    h_jt = H_JT()


    ## total hamiltonian  operator
    #################################
    H = h_ir + h_jt + h_coupling
    #################################


    ## diagonalize helmitian
    
    Hmtrx = op2mtrx(bases, H, bases)

    E, C = diagonalize_helmitian_operator(Hmtrx)

    ### Save files
    # path to result folder
    path2svFolder = os.path.join(ROOTPATH, 'irsim', 'result')

    # current time
    now = datetime.datetime.now()

    # get save directory name (eg. 96H96_180123_19000)
    svDirName = create_dir_name(bases, bases, now)

    # path to the save directory
    p2d = os.path.join(path2svFolder, svDirName)

    # create the save directory
    os.makedirs(p2d, exist_ok=True)

    # save files
    with open(os.path.join(p2d, 'BasesKet.dill'), 'wb') as f:
        dill.dump(bases, f)

    with open(os.path.join(p2d, 'BasesBra.dill'), 'wb') as f:
        dill.dump(bases, f)

    with open(os.path.join(p2d, 'mtrx.dill'), 'wb') as f:
        dill.dump(Hmtrx, f)

    with open(os.path.join(p2d, 'E.dill'), 'wb') as f:
        dill.dump(E, f)

    with open(os.path.join(p2d, 'C.dill'), 'wb') as f:
        dill.dump(C, f)

    # set parameters
    svConst = {
        'IR_LIMIT': IR_LIMIT,
        'INEQUALITY': INEQUALITY,
        'DIC_COUPLING_CONSTANT': DIC_COUP_CONST,
        'DIC_QUADRATIC_MATRIX': DIC_Q_MTRX,
        'DIC_IR_FREQUENCY': DIC_IR_FREQ,
        'DIC_COUPLING_CONSTANT': DIC_COUP_CONST,
        'DIC_VIBRONIC_ENERGY_LEVEL': DIC_JT_EE,
        'DIC_REDUCED_MATRIX_ELEMENT': DIC_RME,
        'DIC_COUPLING_MATRIX': DIC_COUP_MTRX,
    }

    with open(os.path.join(p2d, 'Constant.dill'), 'wb') as f:
        dill.dump(svConst, f)

    svOperator = {
            'q': q,
            'Q': Q,
            'H_coupling': H_coupling,
            'H_IR': H_IR,
            'H_JT': H_JT,
            'hamiltonian': H,
            }

    with open(os.path.join(p2d, 'Operator.dill'), 'wb') as f:
        dill.dump(svOperator, f)

    print('Saved in {} directory'.format(svDirName))
    print('Done.')

