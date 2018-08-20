import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator
from irsim.quantum_operator import CreationOperator, AnnihilationOperator


'''
Contents:
    (1) PositionalOperator (class)
'''


class PositionalOperator(QuantumOperator):
    @classmethod
    def set_ir_frequency(cls, DIC):
        '''dict data of IR frequency is in CONSTANT.py file. The format
        is like this:
        DIC_IR_FREQUENCY = {
                Key(mode='t1u', modeNum=4): 0.00629777152672,
                }
        '''
        cls.DIC_IR_FREQUENCY = DIC

    def __init__(self, mode, lvl, orb=None):
        self.mode = mode
        self.lvl = lvl
        self.orb = orb

        if orb is not None:
            self.cre = CreationOperator(mode, lvl, orb)
            self.ann = AnnihilationOperator(mode, lvl, orb)

            try: 
                self.omega = self.DIC_IR_FREQUENCY[(mode, lvl)]

            except AttributeError as e:
                print(e, 'Set IR frequency data (use set_IR_frequency method)')

            qop = (np.sqrt(self.HBAR / (2 * self.omega))
                    * (self.cre + self.ann))

            self.operator = qop.operator

    def __iter__(self):
        gen = (PositionalOperator(self.mode, self.lvl, orb) 
                for orb in super().ORBITAL[self.mode[:-1]]) # mode t1u -> t1
        return gen
