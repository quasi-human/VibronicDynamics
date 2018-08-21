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
