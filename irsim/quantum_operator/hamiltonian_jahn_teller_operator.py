import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator, copy

'''
Contents:
    (1) HamiltonianJahnTellerOperator (class)
'''


class HamiltonianJahnTellerOperator(QuantumOperator):

    @classmethod
    def set_jt_eigen_energy(cls, DIC):
        '''dict data of eigen energy is in CONSTANT.py file. The format
        is like this:
        DIC_IR_FREQUENCY = {
                Key(mode='t1u', modeNum=4): 0.00629777152672,
                }
        '''

        cls.DIC_JT_EIGEN_ENERGY = DIC

    def __init__(self):
        pass
        
    @copy
    def operator(self, ket):
        energy = 0
        for e in ket:
            if e.QUANTUM_TYPE != 'JT':
                continue
            Alpha, J, _, P = e.qval
            energy = self.DIC_JT_EIGEN_ENERGY[(Alpha, J, P)]
        ket.weight *= energy
        yield ket
