import numpy as np
import os
import sys
ROOTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(ROOTPATH)
from irsim.core import QuantumOperator
from irsim.quantum_operator import PositionalOperator

'''
Contents:
    (1) QuantumOperator (class)
'''

class CubicOperator(QuantumOperator):
    @classmethod
    def set_quadratic_matrix(cls, DIC):
        '''dict data of QUADRATIC MATRIX is in QUADRATIC_MATRIX.py file.
        The format is like this:
        DIC_QUADRATIC_MATRIX = {
                Key('hg', 't1', 't1', 1, 'theta'):
                    sqrt(1/6) * np.array([
                            [ -1,  0,  0],
                            [  0, -1,  0],
                            [  0,  0,  2]]),
                    }
        '''

        cls.DIC_QUADRATIC_MATRIX = DIC

    def __init__(self, qopL, cmb, qopR, Qmode=None):
        ''' The example of cmb: ('hg', 't1', 't1', 1)
        qopL: left QuantumOperator instance
        qopR: right QuantumOperator instance
        Qmode is like 'theta' etc.
        '''

        self._qopL = qopL
        self._rqop = qopR

        if isinstance(qopL, PositionalOperator):
            self.modeL = self._qopL.mode
            self.lvlL = self._qopL.lvl
        elif isinstance(qopL, type(self)):
            pass

        if isinstance(qopR, PositionalOperator):
            self.modeR = self._rqop.mode
            self.lvlR = self._rqop.lvl
        elif isinstance(qopR, type(self)):
            pass

        self.arL = np.array(list(qopL)) # 1d array whose elements are qop
        self.cmb = cmb # a part of a key of DIC_QUADRATIC_MATRIX
        self.LAMBDA, self.gammaL, self.gammaR, self.vlvl = self.cmb
        self.arR = np.array(list(qopR))

        if Qmode is not None:
            self.Qmode = Qmode

            QMKey = (*cmb, Qmode)
            self.Qmtrx = self.DIC_QUADRATIC_MATRIX[QMKey]

            qop = (self.arL).dot(self.Qmtrx).dot(self.arR)

            qop = self._clean(qop) # unite the same ket

            self.operator = qop.operator

    def __iter__(self):
        Qmodes = super().ORBITAL[self.LAMBDA[:-1]] # hg -> h

        gen = (QuadraticOperator(self.arL, self.cmb, self.arR, Qmode)
                for Qmode in Qmodes)
        return gen

if __name__ == '__main__':
    from irsim.database import import_vibronic_coupling_matrix
    path = os.path.join(ROOTPATH, 'irsim/database/HIRmat_hghg1.dat')
    d = import_vibronic_coupling_matrix(path)
    print(d)




