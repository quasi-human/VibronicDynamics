import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import QuantumOperator, copy
from irsim.quantum_basis import JahnTellerState


'''
Contents:
    (1) JahnTellerTransitOperator (class)
'''


#class JahnTellerTransitOperator(QuadraticOperator):
class JahnTellerTransitOperator(QuantumOperator):
    def __init__(self, toAlpha, toJ, toM, toP): 
        self.toJT = JahnTellerState(Alpha=toAlpha, J=toJ, M=toM, P=toP)

    @copy
    def operator(self, ket):
        ket[('JT',)].qval = self.toJT 
        yield ket
