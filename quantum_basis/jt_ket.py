from collections import namedtuple
import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import Ket


'''
Contents:
    (1) JahnTellerKet (class)
'''


JahnTellerState = namedtuple('JahnTellerState', 'Alpha, J, M, P')

class JahnTellerKet(Ket):
    QUANTUM_TYPE = 'JT'

    @classmethod
    def set_alpha_j_p_combinations(cls, combinations):
        cls.ALPHA_J_P_COMBINATIONS = sorted(combinations)

    def __init__(self, Alpha=None, J=None, M=None, P=None):
        qval = (Alpha, J, M, P)

        # store initially given parameters
        init_args = {'Alpha': Alpha, 'J': J, 'M': M, 'P': P}

        # make identifier among other ket
        key = (self.QUANTUM_TYPE,)

        super().__init__(qval=qval, init_args=init_args, key=key)

    @property
    def qval(self):
        return self._qval

    @qval.setter
    def qval(self, val):
        if not isinstance(val, tuple):
            raise ValueError('qval must be immutable.')
        self._qval = JahnTellerState(*val)

    def __iter__(self):
        for Alpha, J, P in self.ALPHA_J_P_COMBINATIONS:
            for M in range(-J, J + 1):
                yield JahnTellerKet(Alpha=Alpha, J=J, M=M, P=P)
