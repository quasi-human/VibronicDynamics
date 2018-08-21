import numpy as np
import os
import pickle
import sys
from time import time
ROOTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
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


'''
Contents:
    (1) op2mtrx (function)
    (2) is_symmetric (function)
    (3) is_diagonalized (function)
    (4) diagonalize_helmitian_operator (function)
'''


def op2mtrx(leftBases, qop, rightBases):
    '''This function converts quantum operator to matrix. Arguments are
    (1) left bases (length: NL)
    (2) quantum operator (QuantumOperator instance)
    (3) right bases (length: NR)
    The obtained matrix size would be NL * NR
    '''

    NR, NL = rightBases.N, leftBases.N # number of ket in bases

    mtrx = np.zeros((NL, NR)) # add clac result on this matrix

    print('**********************************************')
    print('Matrix Representation of Quantum Operators')
    print('**********************************************')
    print('Shape: |{NL}><{NL}|{qop}|{NR}><{NR}|'
            .format(NL=NL, qop=qop.__class__.__name__, NR=NR))
    print('Processing...\n')
    print('Progress', 'Duration', 'Speed', sep='\t')
    print('----------------------------------------------')

    st = time()
    scanned = 1
    for rightIndex, ket in enumerate(rightBases):
        for opket in qop(ket):
            try:
                leftIndex = leftBases.get_index_from_ket(opket)

            # case that there is no corresponding ket in rightBases
            except ValueError:
                #print('No exist', opket.qval) # for debug
                continue # ignore the missing ket

            mtrx[leftIndex, rightIndex] += opket.weight

        # display duration time and speed
        if (rightIndex == scanned - 1) or (rightIndex == NR - 1):
            lt = time()
            print('{cur:5d} / {NR}'.format(cur=rightIndex + 1, NR=NR), 
                    '{dur:5.1f} (s)'.format(dur=(lt - st)),
                    '{speed:1.3f} (s/ket)'.format(
                        speed=(lt - st)/(rightIndex + 1)),
                    sep='\t')

            scanned *= 2

    print('----------------------------------------------')
    print('\nDone.\n')
    return mtrx


def is_symmetric(mtrx): # mtrx is ndarray
    nrow, ncol = mtrx.shape
    if nrow != ncol:
        return False
    arDiff = mtrx - mtrx.T # original - transposed matrix
    numError = np.sum(arDiff != 0) // 2 # the number of non-zero pair
    if numError == 0:
        return True
    else:
        return False


def is_diagonalized(mtrx): # mtrx is ndarray
    if np.sum(mtrx - np.diag(np.diagonal(mtrx)) != 0) == 0:
        return True
    else:
        return False


def diagonalize_helmitian_operator(mtrx):
    print('**********************************************')
    print('Diagonalization of Helmitian Matrix')
    print('**********************************************')
    # check dimension
    if mtrx.ndim != 2:
        raise ValueError('Dimension is invalid.')
    
    # check symmetry
    print('Is symmetric?')
    print('----------------------------------------------')
    if is_symmetric(mtrx):
        print('\tYES.\n')
    else:
        print('\tNO.\n')
        raise ValueError('The given matrix is not Hermitian')

    # check diagonalized
    print('Is already diagonalized?')
    print('----------------------------------------------')
    if is_diagonalized(mtrx):
        print('\tYES.\n')
    else:
        print('\tNO.\n')
        print('Processing...\n')

    res = np.linalg.eigh(mtrx)
    print('Done.\n')

    return res
