import os
import sys
sys.path.append(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from irsim.core import Ket 


'''
Contents:
    (1) InfraredKet (class)
    (2) create_ir_ket_filter (function)
'''


class InfraredKet(Ket):
    QUANTUM_TYPE = 'IR'

    DIC_IR_ORB = {
            't1u': ('x', 'y', 'z'),
            'gu': ('a', 'x', 'y', 'z'),
            'hu': ('theta', 'epsilon', 'xi', 'eta', 'zeta')
            }

    INF = 20 # excitation limit (default)

    def __init__(self, mode, modeNum, orb=None, qval = None,
            excitation_limit = INF):
        '''Determine the initial state of IR ket.
        '''

        # mode: IR mode. eg.) "t1u", "gu" etc. (string)
        self.mode = mode

        # modeNum: IR mode number. eg.) 4, 5 etc. (integer)
        self.modeNum = int(modeNum)

        # orb (option): IR orbital eg.) "x", "theta" etc. (string)
        self.orb = orb

        # excitation upper limit
        self.excitation_limit = excitation_limit

        # allow +1 level excitation at intermediate process.
        self._intermediate_limit = self.excitation_limit + 1

        # keep given arguments at instantiation.
        # the reason why qval is not included here is that qval can be
        # changed after instantiation by annihilation operator for example.
        init_args = {'mode': mode, 'modeNum': modeNum, 'orb': orb, 
                'excitation_limit': excitation_limit}

        # make identifier among other kets
        key = (self.QUANTUM_TYPE, self.mode, self.modeNum, self.orb)

        # initialize Ket (parent class)
        super().__init__(qval=qval, init_args=init_args, key=key)

        # extract symetry info
        self.group = self.mode[:-1] # eg. "t1"
        self.gerade = self.mode[-1] # eg. "u"

    @property
    def qval(self):
        return self._qval

    @qval.setter
    def qval(self, val):
        if not isinstance(val, int):
            if val is None:
                self._qval = None
            else:
                raise ValueError('qval must be integer.')
        elif (self._intermediate_limit < val) or (val < 0):
            raise ValueError('Input value is over the intermediate limit.')
        else:
            self._qval = val

    def __iter__(self):
        if self.orb is None: # generate ket with the whole orbitals
            ORBS = self.DIC_IR_ORB[self.mode] # eg.) ('x', 'y', 'z')
            for orb in ORBS:
                yield InfraredKet(self.mode, self.modeNum, orb, None,
                        self.excitation_limit)

        else: # generate ket with serial excitation level
            for qval in range(self.excitation_limit + 1):
                yield InfraredKet(self.mode, self.modeNum, self.orb, 
                        qval, self.excitation_limit)

                    
def create_ir_ket_filter(inequality, sum_limit):
    '''Closure. This function returns function which evaluate 
    the sum of IR excitation level (sum_limit). Users can choose
    '==' or '<=' as inequality of the imposed condition.'''

    if inequality in ('=', '=='): # case: equal
        is_true = lambda x: x == sum_limit
    elif inequality == '<=': # case: equal or less than
        is_true = lambda x: x <= sum_limit
    else:
        raise ValueError('Choose ==, <=')

    def filter_ir_ket(productKet):
        '''This filter works against productKet which is not in accordance
        with imposed condition(s).'''

        # check productKet has IR state
        setLabel = set(ket.keys[0][0] for ket in productKet)
        if 'IR' not in setLabel:
            return True # pass everything.

        # calculate total excitation
        tot = sum(ket._qval for ket in productKet if ket.keys[0][0] == 'IR')
        return is_true(tot)

    return filter_ir_ket
