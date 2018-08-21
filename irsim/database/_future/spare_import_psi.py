#import numpy as np
import sys
from collections import namedtuple
sys.path.append('/home/yuki/project/sympy/sympy/parsing/')
from mathematica import mathematica as mm


# Greek to plain
_G2P = {
        'θ': 'theta',
        'ε': 'epsilon',
        'ϵ': 'epsilon',
        'ξ': 'xi',
        'η': 'eta',
        'ζ': 'zeta',
        #'α': 'Alpha',
        }

def _convert_greek_letter(s):
    s = s.replace(' ', '')
    if s in _G2P:
        return _G2P[s]
    else:
        return s


def import_psi(path):
    g2p = _convert_greek_letter
    setSym = ('a', 't1', 't1', 'g', 'h')
    Psi = namedtuple('Psi', ('Gamma1', 'gamma1', 'Gamma2', 'gamma2', 'n', 'Gamma', 'gamma'))

    d = {}

    with open(path, 'r') as f:
        for line in f:
            # ignore comments and return 
            if line[0] in ('#', '\n'):
                continue

            # delete \n and split to list
            G1, g1, G2, g2, G, g, coef = line.rstrip().split('\t')

            nG = G.split()
            
            if len(nG) == 1:
                n = 1
                G = nG[0]
            elif len(nG) == 2:
                n = nG[0]
                G = nG[1]
            else:
                raise ValueError('Gamma is invalid')

            # convert mathematica expresstion to python
            psi = Psi(G1, g2p(g1), G2, g2p(g2), n, G, g2p(g))
            d[psi] = float(mm(coef))
            
            #print(*psi)
            #print(psi)

    return d


if __name__ == '__main__':
    PATH = r'Psi.dat'
    DIC = import_psi(PATH)

    print(DIC)





