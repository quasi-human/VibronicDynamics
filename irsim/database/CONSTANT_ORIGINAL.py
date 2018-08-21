import inspect
import os
import sys
import numpy as np
from collections import namedtuple
try:
    from import_vibronic_energy_levels import import_vibronic_energy_levels
    from import_matrix import import_dic_coupling_matrix
except ImportError:
    from .import_vibronic_energy_levels import import_vibronic_energy_levels
    from .import_matrix import import_dic_coupling_matrix

#############################
# DO NOT CHANGE VALUES HERE #
#############################
HBAR = 1 # (au)
AU2EV = 27.2113961 # (eV/au)
SPEED_OF_LIGHT = 3e8 # (m/s)
SI2AU_TIME = 4.134137457575e16 # (time in a.u./s)
SI2AU_ENERGY = 2.2937126583579e17 # (energy in a.u./ J)
WVN2AU = SI2AU_TIME**(-1) * SPEED_OF_LIGHT * 100 * 2 * np.pi
KB = SI2AU_ENERGY * 1.380e-23 # Boltzman constant

# get this file path (absolute path to the directory which contains this file.)
THIS_FILE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

Key = namedtuple('Key', 'mode modeNum')
# frequency for hamiltonian of IR
DIC_IR_FREQUENCY = {
        Key(mode='t1u', modeNum=4):0.00629777152672,
        Key(mode='gu', modeNum=5): 0.00607391422943, # gu(5)
        Key(mode='gu', modeNum=6): 0.00654888037462, # gu(6)
        Key(mode='hu', modeNum=6): 0.00618765654550,
        Key(mode='hg', modeNum=1): 0.00123794306479,
        Key(mode='hg', modeNum=2): 0.00198967498374,
        Key(mode='hg', modeNum=3): 0.00318915063041,
        Key(mode='hg', modeNum=4): 0.00358652618172,
        Key(mode='hg', modeNum=5): 0.00513769023393,
        Key(mode='hg', modeNum=6): 0.00578800398001,
        Key(mode='hg', modeNum=7): 0.00648787205574,
        Key(mode='hg', modeNum=8): 0.00711775363613,
        }

# frequency for hamiltonian of IR
#DIC_IR_FREQUENCY = {
#        't1u': {
#            4: 0.00629777152672 * 1.0,
#            },
#        'gu' : {
#            5: 0.00607391422943, # gu(5)
#            #'6': 0.00654888037462, # gu(6)
#            },
#        'hu': {
#            6: (0.00618765816848 + 0.00618765492253)/2,
#            },
#        'hg': {
#            1: 0.00123794306479,
#            2: 0.00198967498374,
#            3: 0.00318915063041,
#            4: 0.00358652618172,
#            5: 0.00513769023393,
#            6: 0.00578800398001,
#            7: 0.00648787205574,
#            8: 0.00711775363613,
#            }
#        }

# coupling constant 
DIC_COUPLING_CONSTANT = {
        # two same mode (notice 1/2 for the same mode)
        (('t1u', 4), ('t1u', 4), 1): -0.000000713859624 , # Gamma = t1u(4), Gamma' = t1u(4), level: 1
        (('gu' , 5), ('gu' , 5), 1): -0.000000377046225 , # Gamma = gu(5), Gamma' = gu(5), level: 1
        (('gu' , 6), ('gu' , 6), 1):  0.000000251113084 , # Gamma = gu(6), Gamma' = gu(6), level: 1
        (('hu' , 6), ('hu' , 6), 1): -0.000000488587363 , # Gamma = hu(6), Gamma' = hu(6), level: 1
        (('hu' , 6), ('hu' , 6), 2):  0.000000041204651 , # Gamma = hu(6), Gamma' = hu(6), level: 2
        #(('hg' , 1), ('hg' , 1), 1): -1.8595708672189756e-08 , 
        #(('hg' , 1), ('hg' , 1), 2): -5.4559126848980821e-09 ,
	#(('hg' , 2), ('hg' , 2), 1):  4.7603885434e-07 ,
	#(('hg' , 2), ('hg' , 2), 2):  1.49592778207e-06 ,
        #(('hg' , 3), ('hg' , 3), 1): -8.03247857346e-07 ,
        #(('hg' , 3), ('hg' , 3), 2): -1.86399811975e-06 ,
        #(('hg' , 4), ('hg' , 4), 1):  7.97357895809e-07 , 
        #(('hg' , 4), ('hg' , 4), 2):  1.8760030609e-06 ,
        #(('hg' , 5), ('hg' , 5), 1): -5.26501224786e-07 , 
        #(('hg' , 5), ('hg' , 5), 2): -9.51905666876e-07 , 
        #(('hg' , 6), ('hg' , 6), 1):  4.66767074012e-07 ,
        #(('hg' , 6), ('hg' , 6), 2):  2.01659325411e-06 , 
        #(('hg' , 7), ('hg' , 7), 1): -3.88856719425e-07 ,
        #(('hg' , 7), ('hg' , 7), 2): -4.78494835508e-07 ,
        #(('hg' , 8), ('hg' , 8), 1):  3.13934489908e-07 ,
        #(('hg' , 8), ('hg' , 8), 2): -6.77415708751e-07 ,

        # two different mode 
        (('t1u', 4), ('gu' , 5), 1):  0.000000637761305  , # Gamma = t1u(4), Gamma' = gu(5), level: 1
       #(('t1u', 4), ('gu' , 6), 1):  0.0000000755364735 , # Gamma = t1u(4), Gamma' = gu(6), level: 1
        (('t1u', 4), ('hu' , 6), 1):  0.00000123545618   , # Gamma = t1u(4), Gamma' = hu(6), level: 1
        (('gu' , 5), ('hu' , 6), 1): -0.000000320887837  , # Gamma = gu(5), Gamma' = hu(6), level: 1
        (('gu' , 5), ('hu' , 6), 2): -0.000000238295052  , # Gamma = gu(5), Gamma' = hu(6), level: 2

        }


W = DIC_IR_FREQUENCY
DIC_CUBIC_COUPLING_CONSTANT = {
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 1) : (1/6) * (1/np.sqrt(W[('hg', 1)])) *  -1.35841731289e-08,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 2) : (1/6) * (1/np.sqrt(W[('hg', 1)])) *   4.58432040867e-09,
	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 1) : (1/6) * (1/np.sqrt(W[('hg', 2)])) *   4.18767466248e-07,
	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 2) : (1/6) * (1/np.sqrt(W[('hg', 2)])) *  -5.03638247517e-07,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 1) : (1/6) * (1/np.sqrt(W[('hg', 3)])) *  -2.08752841004e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 2) : (1/6) * (1/np.sqrt(W[('hg', 3)])) *   5.99015740882e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 1) : (1/6) * (1/np.sqrt(W[('hg', 4)])) *   4.40781013983e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 2) : (1/6) * (1/np.sqrt(W[('hg', 4)])) *  -5.12317985399e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 1) : (1/6) * (1/np.sqrt(W[('hg', 5)])) *  -1.87912594131e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 2) : (1/6) * (1/np.sqrt(W[('hg', 5)])) *   4.38642817653e-07 , 
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 1) : (1/6) * (1/np.sqrt(W[('hg', 6)])) *   4.42720912624e-07 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 2) : (1/6) * (1/np.sqrt(W[('hg', 6)])) *  -5.03623945963e-07 , 
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 1) : (1/6) * (1/np.sqrt(W[('hg', 7)])) *  -6.57468785510e-08 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 2) : (1/6) * (1/np.sqrt(W[('hg', 7)])) *   8.13496850456e-09 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 1) : (1/6) * (1/np.sqrt(W[('hg', 8)])) *  -2.89198940728e-08 ,
        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 2) : (1/6) * (1/np.sqrt(W[('hg', 8)])) *  -3.19180761379e-08 ,
        }

# WITHOUT EMPLOYING TEMPORARY TERMS
#DIC_CUBIC_COUPLING_CONSTANT = {
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 1) : (1/6) * (1/np.sqrt(W['hg'][1])) *  -2.7702893161846379e-08,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 2) : (1/6) * (1/np.sqrt(W['hg'][1])) *   3.0235949438851033e-08,
#	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 1) : (1/6) * (1/np.sqrt(W['hg'][2])) *  -6.9765483882e-08,
#	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 2) : (1/6) * (1/np.sqrt(W['hg'][2])) *  -3.84655946775e-07,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 1) : (1/6) * (1/np.sqrt(W['hg'][3])) *  -7.08493919644e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 2) : (1/6) * (1/np.sqrt(W['hg'][3])) *   6.20752088459e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 1) : (1/6) * (1/np.sqrt(W['hg'][4])) *   2.28744288384e-09 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 2) : (1/6) * (1/np.sqrt(W['hg'][4])) *  -5.95086336581e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 1) : (1/6) * (1/np.sqrt(W['hg'][5])) *  -2.29070719403e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 2) : (1/6) * (1/np.sqrt(W['hg'][5])) *   1.26082708506e-07 , 
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 1) : (1/6) * (1/np.sqrt(W['hg'][6])) *  -3.30235824179e-09 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 2) : (1/6) * (1/np.sqrt(W['hg'][6])) *  -6.34028717425e-07 , 
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 1) : (1/6) * (1/np.sqrt(W['hg'][7])) *  -5.91514047192e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 2) : (1/6) * (1/np.sqrt(W['hg'][7])) *  -2.21963395595e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 1) : (1/6) * (1/np.sqrt(W['hg'][8])) *  -4.24779175716e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 2) : (1/6) * (1/np.sqrt(W['hg'][8])) *  -7.76934476903e-10 ,
#        }

## WITHOUT EMPLOYING TEMPORARY TERMS
#DIC_K_CUBIC_CONSTANT = {
#        (('t1u', 4), ('t1u', 4), ('hg', 1)) :  1.97716075344e-09,
#	(('t1u', 4), ('t1u', 4), ('hg', 2)) : -4.60335915506e-08,
#        (('t1u', 4), ('t1u', 4), ('hg', 3)) :  3.43029082858e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 4)) : -4.75885414940e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 5)) :  2.73538393962e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 6)) : -4.03727550286e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 7)) : -4.31671701383e-09 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 8)) : -1.76357584131e-09 ,
#        }

# WITHOUT EMPLOYING TEMPORARY TERMS
DIC_K_CUBIC_CONSTANT = {
        (('t1u', 4), ('t1u', 4), ('hg', 1)) : (1/2) * (1/np.sqrt(W[('hg', 1)])) *  1.97716075344e-09,
	(('t1u', 4), ('t1u', 4), ('hg', 2)) : (1/2) * (1/np.sqrt(W[('hg', 2)])) * -4.60335915506e-08,
        (('t1u', 4), ('t1u', 4), ('hg', 3)) : (1/2) * (1/np.sqrt(W[('hg', 3)])) *  3.43029082858e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 4)) : (1/2) * (1/np.sqrt(W[('hg', 4)])) * -4.75885414940e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 5)) : (1/2) * (1/np.sqrt(W[('hg', 5)])) *  2.73538393962e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 6)) : (1/2) * (1/np.sqrt(W[('hg', 6)])) * -4.03727550286e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 7)) : (1/2) * (1/np.sqrt(W[('hg', 7)])) * -4.31671701383e-09 ,
        (('t1u', 4), ('t1u', 4), ('hg', 8)) : (1/2) * (1/np.sqrt(W[('hg', 8)])) * -1.76357584131e-09 ,
        }

DIC_K_CUBIC_CONSTANT = {
        (('t1u', 4), ('t1u', 4), ('hg', 1)) : (1/2) * (1/np.sqrt(W[('hg', 1)])) *  3.7978166779690897e-09,
	(('t1u', 4), ('t1u', 4), ('hg', 2)) : (1/2) * (1/np.sqrt(W[('hg', 2)])) * -7.02148059216e-09,
        (('t1u', 4), ('t1u', 4), ('hg', 3)) : (1/2) * (1/np.sqrt(W[('hg', 3)])) *  7.11437067912e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 4)) : (1/2) * (1/np.sqrt(W[('hg', 4)])) * -1.84193247246e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 5)) : (1/2) * (1/np.sqrt(W[('hg', 5)])) *  2.07717875336e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 6)) : (1/2) * (1/np.sqrt(W[('hg', 6)])) * -1.20770157846e-08 ,
        (('t1u', 4), ('t1u', 4), ('hg', 7)) : (1/2) * (1/np.sqrt(W[('hg', 7)])) * -5.75395347576e-09 ,
        (('t1u', 4), ('t1u', 4), ('hg', 8)) : (1/2) * (1/np.sqrt(W[('hg', 8)])) *  1.47258265454e-10 ,
        }

#DIC_CUBIC_COUPLING_CONSTANT = {
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 1) : (1/6) *  -2.7702893161846379e-08,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 1), 2) : (1/6) *   3.0235949438851033e-08,
#	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 1) : (1/6) *  -6.9765483882e-08,
#	((('t1u', 4), ('t1u', 4), 1), ('hg', 2), 2) : (1/6) *  -3.84655946775e-07,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 1) : (1/6) *  -7.08493919644e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 3), 2) : (1/6) *   6.20752088459e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 1) : (1/6) *   2.28744288384e-09 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 4), 2) : (1/6) *  -5.95086336581e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 1) : (1/6) *  -2.29070719403e-07 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 5), 2) : (1/6) *   1.26082708506e-07 , 
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 1) : (1/6) *  -3.30235824179e-09 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 6), 2) : (1/6) *  -6.34028717425e-07 , 
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 1) : (1/6) *  -5.91514047192e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 7), 2) : (1/6) *  -2.21963395595e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 1) : (1/6) *  -4.24779175716e-08 ,
#        ((('t1u', 4), ('t1u', 4), 1), ('hg', 8), 2) : (1/6) *  -7.76934476903e-10 ,
#        }

#DIC_K_CUBIC_CONSTANT = {
#        (('t1u', 4), ('t1u', 4), ('hg', 1)) : (1/2) *  3.7978166779690897e-09,
#	(('t1u', 4), ('t1u', 4), ('hg', 2)) : (1/2) * -7.02148059216e-09,
#        (('t1u', 4), ('t1u', 4), ('hg', 3)) : (1/2) *  7.11437067912e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 4)) : (1/2) * -1.84193247246e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 5)) : (1/2) *  2.07717875336e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 6)) : (1/2) * -1.20770157846e-08 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 7)) : (1/2) * -5.75395347576e-09 ,
#        (('t1u', 4), ('t1u', 4), ('hg', 8)) : (1/2) *  1.47258265454e-10 ,
#        }


#DIC_K_CONSTANT = {
#        ('t1u', 4, 4): -4.7517390604836306e-07,
#        ('hg', 1, 1) : -6.5903435588980407e-09,
#	('hg', 2, 2) : -7.7332171687e-08,
#        ('hg', 3, 3) : -2.98802253678e-07 ,
#        ('hg', 4, 4) : -1.53919200046e-08 ,
#        ('hg', 5, 5) : -1.00037838178e-07 , 
#        ('hg', 6, 6) : -1.96891388444e-07 , 
#        ('hg', 7, 7) : 1.38049054848e-07 ,
#        ('hg', 8, 8) : -1.75493709193e-07 ,
#        }

#DIC_V_CONSTANT = {
#        ('hg', 1) : 1.8994136507816384e-05,
#        ('hg', 2) : 4.34230919275e-05,
#        ('hg', 3) : 8.2273367543e-05 ,
#        ('hg', 4) : 5.34545073042e-05 ,
#        ('hg', 5) : 7.52911857249e-05 ,
#        ('hg', 6) : 5.82402884641e-05 ,
#        ('hg', 7) : 0.000201387883837 ,
#        ('hg', 8) : 0.000204452754312 ,
#        }


# JT transit database
#try:
#    from REDUCED_MATRIX_ELEMENT import DIC_REDUCED_MATRIX_ELEMENT
#except ImportError:
#    from .REDUCED_MATRIX_ELEMENT import DIC_REDUCED_MATRIX_ELEMENT

# IR and JT coupling matrix
FILENAME = THIS_FILE_PATH + '/HIRmat.dat'
COUPLING_MATRIX = import_dic_coupling_matrix(FILENAME)

# cubic term
FILENAME = os.path.join(THIS_FILE_PATH, 'HIRmat_hghg1.dat')
hh1 = import_dic_coupling_matrix(FILENAME)
FILENAME = os.path.join(THIS_FILE_PATH, 'HIRmat_hghg2.dat')
hh2 = import_dic_coupling_matrix(FILENAME)
DIC_CUBIC_COUPLING_MATRIX = {
        1: hh1, # key: hh(n)'s n
        2: hh2,
        }

DIC_XI_CUBIC_AG = {
        (1, 1): {
            1: -1.2867180989406233,
            2: -1.6684095194536435,
            3: -1.5635773708312788,
            4: -0.9863113646341368,
            5: -0.8601018550070318,
            6: -0.5257334581442651,
            7: -1.6996134501825901,
            8: -1.4673693391271558,
            },
        (2, 2): {
            1: -1.4869978346629764,
            2: -1.740972192339494,
            3: -1.5587309503669489,
            4: -0.9788147273008881,
            5: -0.8437983710630573,
            6: -0.5145987434435114,
            7: -1.6610224678588517,
            8: -1.432996519636488,
            },
        }

DIC_XI_CUBIC_HGHG = {
        # hh(1)
        1: { 
            (1, 1): { # J, J'
                1: 0.3993945488293311,
                2: 0.49682699030196253,
                3: 0.443972331490545,
                4: 0.27762386516279736,
                5: 0.23361377337174719,
                6: 0.14095550084829558,
                7: 0.4496955177238998,
                8: 0.38454149001166343,
                },
            (2, 2): { # J, J'
                1: -0.3270223460882328,
                2: -0.3589138906702228,
                3: -0.3019927516453917,
                4: -0.18767124838351212,
                5: -0.15541315213063325,
                6: -0.09347943689738357,
                7: -0.2976184952400321,
                8: -0.2542749671584524,
                },
            },
        # hh(2)
        2: {
            (2, 2): { # J, J'
                1: -0.1441580489638537,
                2: -0.1438489586650541,
                3: -0.10953197858119741,
                4: -0.06687675693604929,
                5: -0.051595934664041304,
                6: -0.030252773896629136,
                7: -0.09384414068886728,
                8: -0.07867677586030497,
                },
            },
        }



#  JT Energy
FILENAME = THIS_FILE_PATH + '/Vibronic_energy_levels.dat'
VIBRONIC_ENERGY_LEVELS = import_vibronic_energy_levels(FILENAME)


## JT CF constant
#DIC_JT_CF = {
#        (1, 2, -1): {
#            (1, 2, -1): {
#                'mtrx': 
#                [[-1/10, 0, 0, 0, -1/2],
#                 [0, 2/5, 0, 0, 0],
#                 [0, 0, -3/5, 0, 0],
#                 [0, 0, 0, 2/5, 0],
#                 [-1/2, 0, 0, 0, -1/10]],
#                'XI': 0.26736,
#                }
#            }
#        }


DIC_JT_CF = {
        (1, 2, -1): {
            (1, 2, -1): {
                'delta': {
                    'E': 0,
                    'T': 0,
                    },
                'distribute': ('E', 'E', 'T', 'T', 'T'),
                'mtrx': np.zeros((5,5)),
                'XI': 0.26736,
                }
            }
        }

def change_dic_jt_cf(fromState, toState, **kwargs):
    d = DIC_JT_CF[fromState][toState]

    # check input
    for lvl, newVal in kwargs.items():
        if lvl not in d['delta']:
            print('Invalid key')
            sys.exit()

        else:
            # over write delta in dictionary
            d['delta'][lvl] = newVal

    # get length of matrix
    N = len(d['distribute'])

    # empty matrix
    mtrx = [[0 for j in range(N)] for i in range(N)]

    # update matrix
    for i in range(N):
        # get splited level name
        lvl = d['distribute'][i]

        # get updated val in each splited level
        val = d['delta'][lvl]

        # overwrite element
        mtrx[i][i] = val

    # overwrite matrix in DIC_JT_CF
    d['mtrx'] = mtrx

    return 

#change_dic_jt_cf((1, 2, -1), (1, 2, -1), E=-2, T=2)
#for k, v in DIC_JT_CF[(1, 2, -1)][(1, 2, -1)].items():
#    if isinstance(v, list):
#        for row in v:
#            print(row)
#        continue
#    print(k)
#    print(v)

if __name__ == '__main__':
    from create_constant_func import show_sorted_vibronic_energy

    # show JT transition table
    print('### Jahn-Teller transition table ###')
    print(DIC_RME, end = '\n\n')

    # show coupling matrix
    print('### IR and JT coupling matrix ###')
    print(COUPLING_MATRIX, end = '\n\n')

    # show eigen energy of JT in acent order 
    print('### JT eigen energy (ascent order) ###')
    show_sorted_vibronic_energy(VIBRONIC_ENERGY_LEVELS)


    print()
    print(DIC_RME[((1,1,1),(1,2,-1))])

    for k, v in DIC_CUBIC_COUPLING_MATRIX.items():
        print(k)
        print(v)
    #sys.exit()
#    from IPython import embed as dbg
#    dbg()
#    COUPLING_MATRIX
