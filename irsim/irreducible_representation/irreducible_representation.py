import itertools
import numpy as np
import os
import sys
from collections import namedtuple
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator, copy


# arguments of IrreducibleRepresentation
IRstate = namedtuple('IRstate', ('mode', 'modeNum', 'ex'))
JTstate = namedtuple('JTstate', ('Alpha', 'J', 'P'))


class IrreducibleRepresentation(QuantumOperator):
    '''One vibrationally excited state is characterized by an irreducible
    representations of an excited mode. This instance creates a matrix 
    operator whose expectations show a contribution of the symmetrized
    vibronic states.'''

    @classmethod
    def set_psi(cls, DIC):
        cls.DIC_PSI = DIC

    def __init__(self, JTstate, IRstate, n, Gamma):
        '''Given 4 arguments determine one symmetrized state.
        (Initial)
        JTstate : Alpha, J, P
        IRstate : mode, modeNum, excitation
        (End)
        n : prefix to a symmetrized mode. eg.) 1 t1, 2 h, 2 g
        Gamma : a symmetrized mode. eg.) t1, h, g
        '''

        self.JTstate = JTstate
        self.IRstate = IRstate
        self.n = n
        self.Gamma = Gamma

    def create_matrix_operator(self, bases):
        '''An argument is not a ket, but bases'''

        # unpack
        mode, modeNum, ex = self.IRstate
        Alpha, J, P = self.JTstate

        mtrx = np.zeros([bases.N, bases.N])

        for gamma in super().ORBITAL[self.Gamma]:
            # mode is like t1u, so mode[:-1] is like t1
            key = (J, mode[:-1], self.n, self.Gamma, gamma)
            val = tuple(self.DIC_PSI[key])

            #|G1,G2,n,G,g><G1,G2,n,G,g| (product sum)
            for (frM, frOrb, frCoef), (
                    toM, toOrb, toCoef) in itertools.product(val, val):
                
                frQval = [] # from
                toQval = [] # to
                for bkey in bases.keys:
                    ## create qval
                    # from value
                    if bkey == ('IR', mode, modeNum, frOrb):
                        frQval.append(1)
                    elif bkey == ('JT',):
                        frQval.append((Alpha, J, frM, P))
                    else:
                        frQval.append(0)
                    # to value
                    if bkey == ('IR', mode, modeNum, toOrb):
                        toQval.append(1)
                    elif bkey == ('JT',):
                        toQval.append((Alpha, J, toM, P))
                    else:
                        toQval.append(0)

                frQval = tuple(frQval)
                toQval = tuple(toQval)

                frInd = bases.get_index_from_qval(frQval)
                toInd = bases.get_index_from_qval(toQval)

                mtrx[frInd, toInd] += toCoef * frCoef

        # return irreducible representation operator in matrix form
        return mtrx
