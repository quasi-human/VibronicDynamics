import sys, os, inspect
import numpy as np
try:
    from MyFuncs import sum_val_in_deepest_dic, merge_coupling_database, squeeze, extract_ir_mode, squeeze_dic_ir_frequency, squeeze_dic_coupling_constant
    #from create_constant_func import merge_coupling_database, squeeze, extract_ir_mode, squeeze_dic_ir_frequency, squeeze_dic_coupling_constant, show_sorted_vibronic_energy
    from import_vibronic_energy_levels import import_vibronic_energy_levels
    from import_matrix import import_dic_coupling_matrix
except ImportError:
    from .MyFuncs import sum_val_in_deepest_dic
    from .create_constant_func import merge_coupling_database, squeeze, extract_ir_mode, squeeze_dic_ir_frequency, squeeze_dic_coupling_constant, show_sorted_vibronic_energy
    from .import_vibronic_energy_levels import import_vibronic_energy_levels
    from .import_matrix import import_dic_coupling_matrix

# get this file path
THIS_FILE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#os.chdir(THIS_FILE_PATH)

# IR limit
IR_LIMIT = 1

#  ('<=' or '=') which determines (sum of IR states) <= IR_LIMIT or (sum of IR states) == IR_LIMIT
INEQUALITY = '<='

# Dirac constant
HBAR = 1

# Golden ratio
GR = (1 + np.sqrt(5))/2

# Mass
M = 1

# Access key to value in state. This order critically affects binary serch of ket.
ACCESS_KEY = (
        ('state', 'IR', 't1u', 'x'),
        ('state', 'IR', 't1u', 'y'),
        ('state', 'IR', 't1u', 'z'),
        ('state', 'IR', 'gu', 'x'),
        ('state', 'IR', 'gu', 'y'),
        ('state', 'IR', 'gu', 'z'),
        ('state', 'IR', 'gu', 'a'),
        ('state', 'IR', 'hu', 'theta'),
        ('state', 'IR', 'hu', 'epsilon'),
        ('state', 'IR', 'hu', 'xi'),
        ('state', 'IR', 'hu', 'eta'),
        ('state', 'IR', 'hu', 'zeta'),
        ('state', 'JT', 'Alpha'),
        ('state', 'JT', 'J'),
        ('state', 'JT', 'M'),
        ('state', 'JT', 'P'),
        )

IR_MODES = extract_ir_mode(ACCESS_KEY)

# frequency for hamiltonian for ir
DIC_IR_FREQUENCY = {
        't1u': 0.00629797566947 * 1.0,
        'gu' : 0.00607428414352, # gu-5
        #'gu' : 0.00654874522743, # gu-6
        #'hu': (0.006187834 + 0.006188224)/2 * 1.02,
        'hu': (0.006187834 + 0.006188224)/2,
        }

# filter DIC_IR_FREQUENCY based on ACCESS_KEY
DIC_IR_FREQUENCY = squeeze_dic_ir_frequency(ACCESS_KEY, DIC_IR_FREQUENCY)

# dictionary for coupling constant (notice 1/2)
DIC_COUPLING_CONSTANT = {
        'tt':  -0.000000713859624 * (1/2) * 1,
        #'gg':   0.000000251113084 * (1/2), #gu(6)
        'gg':  -0.000000377046225 * (1/2), #gu(5)
        'hh1': -0.000000488587363 * (1/2), 
        'hh2':  0.000000041204651 * (1/2),
       #'tg':   0.0000000755364735 , #t1u - gu(6)
        'tg':   0.000000637761305 * 1, #t1u - gu(5)
        'th':   0.00000123545618  * 1, 
        #'th':   0.00000123545618 , 
        'gh1': -0.000000320887837 * 1, # gu(5) - hu(6) [1]
        'gh2': -0.000000238295052 * 1, # gu(5) - hu(6) [2]
        }
# filter DIC_COUPLING_CONSTANT based on ACCESS_KEY
#DIC_COUPLING_CONSTANT = squeeze_dic_coupling_constant(ACCESS_KEY, DIC_COUPLING_CONSTANT)
#print(DIC_COUPLING_CONSTANT)

#  JT Energy
# get this file path
THIS_FILE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#os.chdir(THIS_FILE_PATH)
FILENAME = THIS_FILE_PATH + '/database/Vibronic_energy_levels.dat'
VIBRONIC_ENERGY_LEVELS = import_vibronic_energy_levels(FILENAME)
#show_sorted_vibronic_energy(VIBRONIC_ENERGY_LEVELS)


# JT transit database
# (Alpha, J, P)
JTTD = {
        ((1, 0, 1), (1, 2, -1)): -0.35921,
        ((1, 0, 1), (2, 2, -1)): -1.24349,
        ((1, 0, 1), (3, 2, -1)): -0.39561,
        ((1, 1, 1), (1, 1, -1)):  0.15160,
        ((1, 1, 1), (2, 1, -1)): -0.20407,
        ((2, 1, 1), (1, 1, -1)):  0.45875,
        ((2, 1, 1), (2, 1, -1)):  0.02322,
        ((3, 1, 1), (1, 1, -1)):  0.15818,
        ((3, 1, 1), (2, 1, -1)):  0.41744,
        ((1, 1, 1), (1, 2, -1)):  1.72566,
        ((1, 1, 1), (2, 2, -1)): -0.35575,
        ((1, 1, 1), (3, 2, -1)):  0.33723,
        ((2, 1, 1), (1, 2, -1)):  0.02215,
        ((2, 1, 1), (2, 2, -1)):  1.16847,
        ((2, 1, 1), (3, 2, -1)): -0.41798,
        ((3, 1, 1), (1, 2, -1)):  0.04677,
        ((3, 1, 1), (2, 2, -1)):  0.08687,
        ((3, 1, 1), (3, 2, -1)):  1.22357,
        ((1, 1, 1), (1, 3, -1)):  0.38879,
        ((1, 1, 1), (2, 3, -1)):  0.40022,
        ((2, 1, 1), (1, 3, -1)):  0.51526,
        ((2, 1, 1), (2, 3, -1)): -0.10170,
        ((3, 1, 1), (1, 3, -1)): -0.06659,
        ((3, 1, 1), (2, 3, -1)): -0.46924,
        ((1, 2, 1), (1, 1, -1)): -0.84799,
        ((1, 2, 1), (2, 1, -1)):  0.017384,
        ((1, 2, 1), (1, 2, -1)): -0.22908,
        ((1, 2, 1), (2, 2, -1)): -0.60145,
        ((1, 2, 1), (3, 2, -1)): -0.09548,
        ((1, 2, 1), (1, 3, -1)): -0.69134,
        ((1, 2, 1), (2, 3, -1)):  0.40301,
        ((1, 3, 1), (1, 1, -1)): -0.77547,
        ((1, 3, 1), (2, 1, -1)):  0.07007,
        ((2, 3, 1), (1, 1, -1)):  0.24950,
        ((2, 3, 1), (2, 1, -1)):  0.69450,
        ((1, 3, 1), (1, 2, -1)): -0.05842,
        ((1, 3, 1), (2, 2, -1)): -0.02920,
        ((1, 3, 1), (3, 2, -1)):  0.05789,
        ((2, 3, 1), (1, 2, -1)): -0.11389,
        ((2, 3, 1), (2, 2, -1)): -0.09077,
        ((2, 3, 1), (3, 2, -1)):  0.08195,
        ((1, 3, 1), (1, 3, -1)): -1.09368,
        ((1, 3, 1), (2, 3, -1)):  0.08915,
        ((2, 3, 1), (1, 3, -1)): -0.18724,
        ((2, 3, 1), (2, 3, -1)): -1.04206,
        ((1, 4, 1), (1, 2, -1)): -0.71939,
        ((1, 4, 1), (2, 2, -1)): -0.56308,
        ((1, 4, 1), (3, 2, -1)):  0.21744,
        ((2, 4, 1), (1, 2, -1)):  0.41509,
        ((2, 4, 1), (2, 2, -1)): -0.63203,
        ((2, 4, 1), (3, 2, -1)): -0.48106,
        ((1, 4, 1), (1, 3, -1)):  0.93543,
        ((1, 4, 1), (2, 3, -1)):  0.15919,
        ((2, 4, 1), (1, 3, -1)):  0.19805,
        ((2, 4, 1), (2, 3, -1)): -0.94502,
        ((1, 4, 1), (1, 6, -1)): -0.99446,
        ((2, 4, 1), (2, 6, -1)): -0.25589,
        ((1, 5, 1), (1, 3, -1)): -0.33406,
        ((1, 5, 1), (2, 3, -1)):  0.03053,
        ((1, 5, 1), (1, 6, -1)): -0.90813,
        }

# restrict JTTD
JTTD = squeeze(JTTD, (1, 1, 1), (1, 2, -1))
#JTTD = squeeze(JTTD, (1, 1, 1), (1, 2, -1), (1, 3, -1))
#JTTD = squeeze(JTTD, (1, 1, 1), (1, 3, -1))
#JTTD = squeeze(JTTD, (1, 1, 1), (1, 2, -1), (1, 3, -1), (1, 4, 1))
#JTTD = squeeze(JTTD, (1, 2, -1), (1, 4, 1))
#JTTD = squeeze(JTTD, (1, 1, 1))
#JTTD = squeeze(JTTD)

# coupling matrix
FILENAME = THIS_FILE_PATH + '/database/HIRmat.dat'
COUPLING_MATRIX = import_dic_coupling_matrix(FILENAME)

# merge coupling 
DIC_JT_COUP = merge_coupling_database(JTTD, COUPLING_MATRIX)
#for k, v in DIC_JT_COUP.items():
#    print(k)
#    if type(v) == list:
#        for e in v:
#            if type(e) == dict:
#                for kk, vv in e.items():
#                    print(kk)
#                    if type(vv) == dict:
#                        for kkk, vvv in vv.items():
#                            print(kkk)
#                            #print(vvv)
#                            for row in vvv:
#                                print(row)
#
#                    else:
#                        print(vv)
#
#
#            else:
#                print(e)
#    else:
#        print(v)


# condtion to IR state (input is cket-dictionary)
#def create_filter_ir_func(condition = '==', *keys):
#    def isTrue(x):
#        if condition == '==':
#            boolean = sum_val_in_deepest_dic(x) == IR_LIMIT
#        elif condition == '<=':
#            boolean = sum_val_in_deepest_dic(x) <= IR_LIMIT
#        else:
#            print("condition sign error. choose '==' or '<='.")
#        return boolean
#
#    def FILTER_IR_FUNC(dic):
#        for key in keys:
#            dic = dic[key] 
#        return isTrue(dic)
#    return FILTER_IR_FUNC

# condtion to JT state (input is cket-dictionary)
def create_filter_jt_func(JTTD):
    setJtComb = set()
    for tups in JTTD.keys():
        for tup in tups:
            setJtComb.add(tup)

    def FILTER_JT_FUNC(jt):
        ret = []
        Alpha = jt['JT']['Alpha']
        J = jt['JT']['J']
        P = jt['JT']['P']
        comb = (Alpha, J, P)
        if len(setJtComb) == 0:
            ret.append(jt)
        if comb in setJtComb:
            ret.append(jt)
        return ret
    return FILTER_JT_FUNC

# set JTTD to FILTER_JT_FUNC
FILTER_JT_FUNC = create_filter_jt_func(JTTD)

if __name__ == '__main__':

    cket = {
            'braket': 'bra',
            'c': 1,
            'state':{
                'IR': {
                    't1u': {
                        'x': 0,
                        'y': 0,
                        'z': 0,
                        },
                    'hu': {
                        'theta': 0,
                        'epsilon': 0,
                        'xi': 0,
                        'eta': 0,
                        'zeta': 0,
                        }
                    },
                'JT': {
                    'Alpha': 1,
                    'J': 1,
                    'M': -1,
                    'P': 1,
                    },
                },
            }


#    print(cket['state']['IR'])
#    FILTER_IR_FUNC = create_filter_ir_func('<=', 'state', 'IR')
#    print(FILTER_IR_FUNC(cket))
#
#
#    FILTER_JT_FUNC = create_filter_jt_func(JTTD)
#
#    print(cket['state'])
#    res = list(filter(FILTER_JT_FUNC, [cket['state']]))
#    print(res)
#
