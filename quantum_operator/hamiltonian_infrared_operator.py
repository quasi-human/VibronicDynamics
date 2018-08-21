import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator, copy


'''
Contents:
    (1) HamiltonianInfraredOperator (class)
'''


class HamiltonianInfraredOperator(QuantumOperator):

    @classmethod
    def set_ir_frequency(cls, DIC):
        '''dict data of IR frequency is in CONSTANT.py file. The format
        is like this:
        DIC_IR_FREQUENCY = {
                Key(mode='t1u', modeNum=4): 0.00629777152672,
                }
        '''

        cls.DIC_IR_FREQUENCY = DIC

    def __init__(self):
        pass
        
    @copy
    def operator(self, ket):
        energy = 0
        for e in ket:
            if e.QUANTUM_TYPE != 'IR':
                continue
            freq = self.DIC_IR_FREQUENCY[(e.mode, e.modeNum)]
            energy += self.HBAR * freq * e.qval
        ket.weight *= energy
        yield ket
