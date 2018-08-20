from copy import deepcopy
from functools import wraps
import itertools
import numpy as np
import os
import sys
from types import MethodType
ROOTPATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../..')
sys.path.append(ROOTPATH)
from irsim.core.core_basis import Ket
from irsim.database.CONSTANT import HBAR


def copy(op):
    '''This decorator does copy instance-ket in order to prevent
    subsequent operation from skewing the original input ket which
    can be used more than once. This issue is related to id. The 
    behavior of deepcopy() is written in a class definition of Ket.'''

    @wraps(op)
    def decorated_operator(self, ket): 
        # duplicate instance
        cp_ket = deepcopy(ket)

        for opket in op(self, cp_ket):
            yield opket

    return decorated_operator


class QuantumOperator(object):
    '''Quntum Operator. This will be a parent of whole other quantum
    operators. Here, define behavior of special method like __add__'''

    GARBAGE_SIZE = 1e-14
    HBAR = HBAR
    GR = (1 + np.sqrt(5)) / 2 # Golden ratio
    ORBITAL = {
            'a': ('a',),
            't1': ('x', 'y', 'z'),
            't2': ('x', 'y', 'z'),
            'g': ('a', 'x', 'y', 'z'),
            'h': ('theta', 'epsilon', 'xi', 'eta', 'zeta'),
            }
    dicFilter = {}

    def __init__(self, unbound_operator=None):
        # Internal Q.O. operator is either a method or Q.O.
        if unbound_operator is not None:
            self.operator = MethodType(unbound_operator, self)
        else:
            self.operator = None
            #raise NotImplementedError

    def __call__(self, ket):
        if self.operator == 0:
            return 0
        return self.operator(ket)

    def __add__(self, x):
        if x == 0:
            return self

        if isinstance(x, QuantumOperator):

            def add_operator(newself, ket):

                # In case of iterable object
                if not isinstance(ket, Ket):
                    # to avoid exhausting generator
                    ket = list(ket)

                for opket in itertools.chain(self(ket), x(ket)):
                    yield opket

        else:
            raise ValueError('Number + Operator is not supported')

        # instante add Quantum operator
        return QuantumOperator(add_operator) 

    def __mul__(self, x):
        if isinstance(x, (int, float)):
            if x == 0:
                return 0 

            #@copy
            def mul_operator(newself, ket):
                # operator is supposed to be pluralized
                for opket in self(ket): 

                    # multiply x and weight
                    opket.weight *= x

                    yield opket 
        
        elif isinstance(x, QuantumOperator):

            def mul_operator(newself, ket): 
                for opket1 in x(ket):
                    for opket2 in self(opket1):
                        yield opket2

        else:
            raise ValueError(
                    '{0} * {1} is not supported'.format(type(self), type(x)))
            
        # instante mul Quantum operator
        return QuantumOperator(mul_operator)

    def __radd__(self, x):
        return self.__add__(x)

    def __rmul__(self, x):
        return self.__mul__(x)

    @classmethod
    def set_filter(cls, label, func):
        cls.dicFilter[label] = func

    @classmethod
    def purge_filter(cls, label=None):
        '''Reset filter function dictionary.'''

        if label is None:
            cls.dicFilter.clear() # set to empty dictionary
        else:
            try:
                del cls.dicFilter[label]
            except KeyError:
                print('"{}" filter function is not registered.'.format(label))
                    
    def _clean(self, x):
        if self.dicFilter:
            def filterFunc(ket):
                for f in self.dicFilter.values():
                    if not f(ket):
                        return False
                return True
        else:
            filterFunc = lambda x: True

        def cleaned_operator(newself, ket):
            '''This function merges kets with the same states to one. '''

            cache = {}
            
            for ket in x(ket): # x(ket) is generator
                if not filterFunc(ket):
                    continue

                if ket.qval not in cache:
                    # add ket to cache
                    cache[ket.qval] = ket
                else:
                    # add weight to existing ket
                    cache[ket.qval].weight += ket.weight

            for ket in cache.values():
                if abs(ket.weight) < self.GARBAGE_SIZE:
                    continue

                yield ket

        # instante clean Quantum operator
        return QuantumOperator(cleaned_operator) 
