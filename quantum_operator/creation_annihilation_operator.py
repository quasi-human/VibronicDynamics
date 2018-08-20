import numpy as np
import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator, copy


'''
Contents:
    (1) CreationAnnihilationOperator (class)
    (2) CreationOperator (class)
    (3) AnnihilationOperator (class)
'''


class CreationAnnihilationOperator(QuantumOperator):
    ''' Creation and Annihilation Operator,
    sign '+' indicates Creation
    sign '-' indicates Annihilation '''
    
    def __init__(self, mode, lvl, orb, sign=None):
        self.mode = mode
        self.lvl = lvl
        self.orb = orb
        self.sign = sign

        if sign is not None:
            self.set_delta(sign)

    def set_delta(self, sign):
        if sign == '+':
            self.deltaKet = +1
            self.deltaC = +1
        elif sign == '-':
            self.deltaKet = -1
            self.deltaC = 0
        else:
            raise ValueError("Input '+' or '-'")

    @copy # necessary because this operator change the qval directly
    def operator(self, ket):
        # get target state
        state = ket['IR', self.mode, self.lvl, self.orb]

        # get excitation level
        exLvl = state.qval

        # change excitation level
        try:
            state.qval += self.deltaKet 
        except ValueError:
            return 

        # multiply eigenvalue and current weight
        ket.weight *= np.sqrt(exLvl + self.deltaC)

        yield ket # use yield. in copy(), for opket in op(self, copiedKet):


class CreationOperator(CreationAnnihilationOperator):
    def __init__(self, mode, lvl, orb):
        super().__init__(mode, lvl, orb, '+')


class AnnihilationOperator(CreationAnnihilationOperator):
    def __init__(self, mode, lvl, orb):
        super().__init__(mode, lvl, orb, '-')
