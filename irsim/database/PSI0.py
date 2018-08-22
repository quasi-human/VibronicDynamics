import inspect
import itertools
import os
import sys
from collections import namedtuple, defaultdict
sys.path.append('/home/yuki/project/sympy/sympy/parsing/')
from mathematica import mathematica as mm


# Greek to plain letters
_G2P = {
        'θ': 'theta',
        'ε': 'epsilon',
        'ϵ': 'epsilon',
        'ξ': 'xi',
        'η': 'eta',
        'ζ': 'zeta',
        }

# convert J to number
_J2N = {
        't1': 1,
        'h': 2,
        }

# convert M to number
_M2N = {
        'x': -1,
        'y': 0,
        'z': 1,
        'theta':-2,
        'epsilon':-1,
        'xi':0,
        'eta':1,
        'zeta':2,
        }

def _convert_greek_letter(s):
    s = s.replace(' ', '')
    if s in _G2P:
        return _G2P[s]
    else:
        return s

def import_psi(path):
    g2p = _convert_greek_letter
    Key = namedtuple('Key', ('Gamma1', 'Gamma2', 'n', 'Gamma', 'gamma'))
    Val = namedtuple('Val', ('gamma1', 'gamma2', 'coef'))

    d = defaultdict(set)

    with open(path, 'r') as f:
        for line in f:
            # ignore comments and return 
            if line[0] in ('#', '\n'):
                continue

            # delete \n  and split to list
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

            # key is (JT, IR, n, Gamma, gamma)
            key = Key(_J2N[G1], G2, int(n), G, g2p(g))

            # convert Mathematica expresstion to Python
            val = Val(_M2N[g2p(g1)], g2p(g2), float(mm(coef)))

            # add value to set
            d[key].add(val)

    return dict(d)


# get this file path (absolute path to the directory which contains this file.)
THIS_FILE_PATH = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))
path = os.path.join(THIS_FILE_PATH, 'Psi0.dat')
DIC_PSI = import_psi(path)
