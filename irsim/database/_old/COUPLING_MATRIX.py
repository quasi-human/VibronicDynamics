from collections import defaultdict
import inspect
import numpy as np
import os
import sys
from sympy.parsing.mathematica import mathematica as mm


def import_vibronic_coupling_matrix(PATH2FILE):
    dd = defaultdict(defaultdict)

    labelStack = []
    rowStack = []
    
    with open(PATH2FILE, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')

            if line[0] == '#': # skip comment lines
                continue

            if not labelStack: # if labelStack is empty
                lJ, rJ, orb = line.split('\t')
                lJ, rJ = int(lJ), int(rJ)
                labelStack.append((lJ, rJ, orb))

                height = 2 * lJ + 1 # Number of matrix row (Matrix hegiht)
                count = 0
                continue

            if count < height:
                count += 1
                row = [float(mm(val)) for val in line.split('\t')]
                rowStack.append(row)

            if count == height:
                lJ, rJ, orb = labelStack.pop()
                dd[(lJ, rJ)][orb] = np.array(rowStack)
                rowStack = []

        return dd


# get this file path (absolute path to the directory which contains this file.)
THIS_FILE_PATH = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))

fn = r'HIRmat.dat'
path = os.path.join(THIS_FILE_PATH, fn)
DIC_COUPLING_MATRIX = import_vibronic_coupling_matrix(path)

fn = r'HIRmat_hghg1.dat'
path = os.path.join(THIS_FILE_PATH, fn)
hh1 = import_vibronic_coupling_matrix(path)

fn = r'HIRmat_hghg2.dat'
path = os.path.join(THIS_FILE_PATH, fn)
hh2 = import_vibronic_coupling_matrix(path)

#print(DIC_COUPLING_MATRIX)
#def generate_line(PATH2FILE):
#    with open(PATH2FILE) as f:
#        for line in f:
#            yield line.rstrip('\n')
#
#def import_dic_coupling_matrix(FILENAME):
#    # import data
#    f = open(FILENAME, 'r')
#    lines = f.read().split('\n')
#    f.close()
#
#    dicMtrx = {}
#
#    while lines:
#        if lines[0] == '':
#            lines.pop(0)
#            continue
#        
#        # jL, jR : JT-J Left, JT-J Right
#        jL, jR, gamma = lines.pop(0).split('\t')
#
#        # convert to integer
#        jL = int(jL)
#        jR = int(jR)
#        
#        # if (jL, jR) pair appers for the first time, then make dictionary
#        if (jL, jR) not in dicMtrx:
#            dicMtrx[(jL, jR)] = {}
#
#        # calculate number of M for jL
#        numRows = 2 * jL + 1
#
#        # empty list for coupling constant matrix
#        l = []
#
#        # read line for height for (jL, jR) matrix
#        for i in range(numRows):
#
#            # empty list for row in coupling constant matrix
#            row = []
#
#            # line is split into element.
#            for e in lines.pop(0).split('\t'):
#                # convert mathematica form to python form
#                if 'Sqrt' in e:
#                    e = e.replace('Sqrt','np.sqrt')
#                if '[' in e:
#                    e = e.replace('[', '(')
#                    e = e.replace(']', ')')
#
#                # evaluate string to float
#                e = eval(e)
#
#                # append float elemnt to row
#                row.append(e)
#
#            # append row to l
#            l.append(row)
#
#        # add l to dictionary
#        dicMtrx[(jL, jR)][gamma] = l
#
#    return dicMtrx
#
#
#
#if __name__ == '__main__':
#    print(mm('Sqrt[2]'))
#    print(mm('-Sqrt[2]'))
#    s = '-3*Sqrt[3/182]'
#    print(mm(s))
#    #sys.exit()
#    FILENAME = r'HIRmat.dat'
#   # FILENAME = r'HIRmat_hghg1.dat'
#   # FILENAME = r'HIRmat_hghg2.dat'
#    PATH = r'/home/yuki/jte/hamiltonian/MyModules/database/'
#    FILENAME = PATH + FILENAME
#
#    PATH2FILE = os.path.join(PATH, FILENAME)
#
##    for e in generate_line(PATH2FILE):
##        print(e)
#
#    #sys.exit()
#
##    import time
##    tt = time.time
##    s = tt()
##    #for _ in range(10000):
##    e = tt()
##    r = mm('Log[2,Log[2, Log[2]]]')
##    print(r)
##    import numpy as np
##    print(np.float(r))
##    print((e-s)/10000)
#    d = import_vibronic_coupling_matrix(PATH2FILE)
#    print(d)
#    #sys.exit()
#    np.set_printoptions(precision=15)
#    for k, v in d.items():
#        if k not in ((1,2), (2,1)):
#            continue
#        print(k)
#        for kk, vv in v.items():
#            print(kk)
#            print(vv)
#        print('==============================')
#
#    import pickle
##    with open('HIRmat.pickle', 'wb') as f:
##        pickle.dump(d, f)
##        print('Saved.')
#    sys.exit()
#    print(d[(1,1)])
    #print(d)
#
#    sys.exit()
#
#    dicMtrx = import_dic_coupling_matrix(FILENAME)
#    
#    for k, v in dicMtrx.items():
#        #if k == (1,2) or k == (2,1):
#        #if k == (1,2) or k == (2,1) or k == (1,1) or k == (2,2):
#            print(k)
#            for gamma in ('theta', 'epsilon', 'xi', 'eta', 'zeta'):
#                print(gamma)
#                mtrx = v[gamma]
#                for e in mtrx:
#                    print(e)
##            for gamma, mtrx in v.items():
##                print(gamma)
##                for e in mtrx:
##                    print(e)
#            print('=============')
#
##
#    for k, v in dicMtrx.items():
#        print(k)
#
#    print(dicMtrx.keys())
#    print(dicMtrx)
