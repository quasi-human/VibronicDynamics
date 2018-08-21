#import numpy as np
import itertools
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


if __name__ == '__main__':
    pass
#    PATH = r'Psi0.dat'
#    DIC = import_psi(PATH)
#
#    # check the number of set for keys of psi dictionary
#    s = set()
#    for k, v in DIC.items():
#        s.add(k[:4])
#    print(len(s))
#    for val in s:
#        print(val)
#
#    DIC_ORB = {
#            'a': ('a',),
#            't1': ('x', 'y', 'z'),
#            't2': ('x', 'y', 'z'),
#            'g': ('a', 'x', 'y', 'z'),
#            'h': ('theta', 'epsilon', 'xi', 'eta', 'zeta'),
#            }
#
#    print()
#    print()
#    print()
#    print()
#    print()
#    #for key1, key2 in itertools.product(s,s):
#    DR0 = {
#            1: 'g',
#            2: 'h',
#            }
#    DR1 = {
#            -2: 'θ',
#            #-1: 'ε',
#            -1: 'ϵ',
#            +0: 'ξ',
#            +1: 'η',
#            +2: 'ζ',
#            }
#    DR2 = {
#            'theta'  : 'θ',
#            #'epsilon': 'ε',
#            'epsilon': 'ϵ',
#            'xi'     : 'ξ',
#            'eta'    : 'η',
#            'zeta'   : 'ζ',
#            'x':'x',
#            'y':'y',
#            'z':'z',
#            }
#
#    for key1, key2 in itertools.combinations_with_replacement(s,2):
#        if key1[0] != key2[0]:
#            continue
#        if key1[1] != key2[1]:
#            continue
#        orbs1 = DIC_ORB[key1[-1]]
#        orbs2 = DIC_ORB[key2[-1]]
#        for orb1, orb2 in itertools.product(orbs1, orbs2):
#            dkey1 = tuple([*key1, orb1])
#            dkey2 = tuple([*key2, orb2])
#            if not dkey1 in DIC:
#                continue
#            if not dkey2 in DIC:
#                continue
#            set1 = DIC[dkey1]
#            set2 = DIC[dkey2]
#            w = 0
#            for v1, v2 in itertools.product(set1, set2):
#                jt1, ir1, coef1 = v1
#                jt2, ir2, coef2 = v2
#                if jt1 == jt2 and ir1 == ir2:
#                    w += coef1 * coef2
#
#            if round(w, 3) not in (0, 1):
#                J1, I1, n1, G1 = key1
#                J2, I2, n2, G2 = key2
#                print(tuple([DR0[J1], I1, n1, G1, DR2[orb1]]), end = ' & ')
#                print(tuple([DR0[J2], I2, n2, G2, DR2[orb2]]))
#                #print(key1, orb1, key2, orb2)
#                print(w)
#
#
#
#    for key in s:
#        for orb in DIC_ORB[key[-1]]:
#            dkey = tuple([*key, orb])
#            w = 0
#            if dkey in DIC:
#                setlis = DIC[dkey]
#                for v in setlis:
#                    w += v.coef**2
#            if round(w,6) != 1:
#            #if w != 1:
#                print(dkey)
#                print(w)
#
#    print()
#    print()
#    print()
#    print()
#    key1 = (2, 'h', 2, 'h', 'xi')
#    key2 = (2, 'h', 1, 'g', 'x')
#    w = 0
#    for v1, v2 in itertools.product(DIC[key1], DIC[key2]):
#        if v1.gamma1 == v2.gamma1 and v1.gamma2 == v2.gamma2:
#            w += v1.coef * v2.coef
#            print(v1, v2)
#
#    print(w)
#    print(DIC.keys())
#        
#
#
#       
#        
#
#    import dill
#    with open('Psi0.dill', 'wb') as f:
#        dill.dump(DIC, f)
#
#
#
#
#
#
