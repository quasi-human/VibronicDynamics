import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator
from irsim.quantum_operator import JahnTellerTransitOperator as JTT


'''
Contents:
    (1) HamiltonianOneCoupling (class)
    (2) HamiltonianCoupling (class)
'''


class HamiltonianOneCouplingOperator(QuantumOperator):

    @classmethod
    def set_coupling_constant(cls, DIC):
        '''dict data of coupling constant is in CONSTANT.py file.
        The format is like this:
        DIC_COUPLING_CONSTANT = {
                (('t1u', 4), ('t1u', 4), 1): -0.000000713859624,
            }
        '''

        HamiltonianOneCouplingOperator.DIC_COUPLING_CONSTANT = DIC

    @classmethod
    def set_coupling_matrix(cls, DIC):
        '''The raw data of coupling matrix is in HIRmat.dat file. 
        The format is Mathematica, hence parsing is necesarry.
        A function, import_vibronic_coupling_matrix(dat_file), converts
        HIRmat.dat file. The obtained format is like this:
        {(1, 1): # J, J'
            {
                'theta': array([[ 0.31622777,  0.        ,  0.        ],
                                [ 0.        ,  0.31622777,  0.        ],
                                [ 0.        ,  0.        , -0.63245553]]), 
                'epsilon': ...
            }
        }
        '''

        HamiltonianOneCouplingOperator.DIC_COUPLING_MATRIX = DIC

        if hasattr(cls, 'DIC_REDUCED_MATRIX_ELEMENT'):
            cls.merge_coupling_matrix_reduced_matrix_element()

    @classmethod
    def set_reduced_matrix_element(cls, DIC):
        '''dictionary data of reduced matrix element is
        in reduced_matrix_element.py
        The format is like this:
        DIC_JT_TRANSITION = {
                # ((Alpha, J, P), (Alpha, J, P)): XI
                (Key(1, 0, 1), Key(1, 2, -1)): -0.35921,
                }
        '''

        HamiltonianOneCouplingOperator.DIC_REDUCED_MATRIX_ELEMENT = DIC

        if hasattr(cls, 'DIC_COUPLING_MATRIX'):
            cls.merge_coupling_matrix_reduced_matrix_element()

    @classmethod
    def merge_coupling_matrix_reduced_matrix_element(cls):
    #def merge_coupling_database(DIC_JT_TRANSIT, DIC_COUP_MTRX):
        '''merge coupling matrix & reduced matrix element'''
        dic = {}

        # transpose matrix for plus keys
        dic_transposed = {}
        for Jpair, v in cls.DIC_COUPLING_MATRIX.items():
            dic_transposed[Jpair] = {} # k is (J, J')

            for mode, mtrx in v.items():
                dic_transposed[Jpair][mode] = mtrx.T # transpose matrix

        for JTpair, XI in cls.DIC_REDUCED_MATRIX_ELEMENT.items():
            pkey = JTpair[0] # shape: ((alpha, J, P = +1), (alpha, J, P = -1))
            nkey = JTpair[1]

            if pkey not in dic:
                dic[pkey] = {}

            dic[pkey][nkey] = {
                    'mtrx': dic_transposed[(pkey.J, nkey.J)],
                    'XI': XI,
                    }

            if nkey not in dic:
                dic[nkey] = {}
            
            dic[nkey][pkey] = {
                    'mtrx': cls.DIC_COUPLING_MATRIX[(pkey.J, nkey.J)],
                    'XI': XI,
                    }

        # rme: reduced matrix element
        HamiltonianOneCouplingOperator.DIC_MATRIX_RME = dic

    def __init__(self, Q): # Q is iterable instance of QuadraticOperator
        self.cache = {}

        self.Q = Q

        # left
        mode1 = Q.modeL
        lvl1 = Q.lvlL

        # right
        mode2 = Q.modeR
        lvl2 = Q.lvlR

        # coupling vibronic level e.g.) hu-hu(2)'s (2)
        vlvl = Q.vlvl

        key = ((mode1, lvl1), (mode2, lvl2), vlvl)

        self.W = self.DIC_COUPLING_CONSTANT[key]

        if mode1 == mode2 and lvl1 == lvl2:
            self.W *= (1/2)

    def operator(self, ket): # JT state transition
        ir_qval = tuple(e.qval for e in ket if e.QUANTUM_TYPE == 'IR')

        # get JT state: (alpha, J, M, P)
        Alpha, J, M, P = ket[('JT',)].qval

        cmbs = ket[('JT',)].ALPHA_J_P_COMBINATIONS

        key = (Alpha, J, P)
        try:
            dicTransit = {}
            for cmb, data in self.DIC_MATRIX_RME[key].items():
                if cmb in cmbs:
                    dicTransit[cmb] = data

        # key error is raised if no combinations are found.
        except KeyError:
            dicTransit = {}

        for Q1 in self.Q:
            # how many quantum types in ket
            sqt = ket.setQuantumType

            if sqt != {'IR', 'JT'}: 
                lisQ1ket = list(Q1(ket)) # no use of cache

            else:
                # cache dict key
                ckey = (ir_qval, ket.weight, Q1.Qmode)

                # use cache of Q(ket)
                if ckey in self.cache:
                    cached = self.cache[ckey]
                
                    # this is not necessary, actually. just for safety.
                    lisQ1ket = []
                    for cket in cached:
                        # recover JT state to the give value
                        for opket in JTT(Alpha, J, M, P)(cket):
                            lisQ1ket.append(opket)

                # register Q(ket) to the cache dictionary
                else:
                    lisQ1ket = list(Q1(ket)) # Q1 doesn't change JT state
                    self.cache[ckey] = lisQ1ket

            # transit is a dict-type
            for toState, transit in dicTransit.items():

                # get to state
                toAlpha, toJ, toP = toState
                mtrx = transit['mtrx'][Q1.Qmode]
                XI = transit['XI']

                # get column in matrix.
                targetColumn = mtrx[:, M+J] # eg. M = -2, J = 2 -> M + J =0

                for i, c in enumerate(targetColumn):
                    # only calculate when matrix element (c) is not zero
                    if c == 0:
                        continue

                    # determine M to which starting ket'M will transit
                    toM = i - toJ

                    # transit jt state
                    JT_transit = JTT(toAlpha, toJ, toM, toP)

                    qop = self.W * XI * c * JT_transit

                    for Q1ket in lisQ1ket:
                        for opket in qop(Q1ket):
                            yield opket

#                    # create quantum opearator
#                    qop = self.W * XI * c * Q1 * JT_transit
#
#                    for opket in qop(ket):
#                        yield opket


class HamiltonianCouplingOperator(HamiltonianOneCouplingOperator):
    def __init__(self, *Qs):
        qop = self._clean(sum(HamiltonianOneCouplingOperator(Q) for Q in Qs))
        self.operator = qop.operator
