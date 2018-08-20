import itertools
from collections import OrderedDict


'''
Contents:
    Ket (class)
    ProductKet (class)
    Bases (class)
    show_ket (function)
'''


class Ket:
    QUANTUM_TYPE = 'QuantumKet'

    def __init__(self, braket='ket',
            weight=1, qval=None, init_args=None, key='Q-state'):
        self.braket = braket # bra or ket
        self.weight = weight
        self.qval = qval # quantum value
        self.init_args = init_args # store initially given arguments
        self.keys = []
        self.dicKet = OrderedDict()
        self._register_ket(key)

    @property
    def qval(self):
        return self._qval

    @qval.setter
    def qval(self, val):
        # qval must be immutable
        if isinstance(val, (int, float, tuple)):
            self._qval = val
        else:
            raise ValueError('qval must be immutable.')

    def _register_ket(self, key):
        self.dicKet[key] = self
        self.keys.append(key)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dicKet[self.keys[key]]
        else: # case qval comes
            return self.dicKet[key]

    def show(self):
        '''Show states of instance'''

        print('==================================================')
        print('WEIGHT : {}'.format(self.weight))
        for key in self.keys:
            print(key, ':',  self[key].qval)
        print('==================================================\n')

    def __deepcopy__(self, memo):
        '''The original deepcopy is well-equipped and slow.
        This method improves the speed of ket instance copying.'''

        cp_ket = type(self)(**self.init_args)
        memo[id(ori_ket)] = self
        cp_ket.qval = self.qval # qval must be immutable

        return cp_productket


class ProductKet(Ket):
    '''Handle multiple kets as a single ket'''

    QUANTUM_TYPE = 'QuantumProductKet'

    def __init__(self, *kets):
        super().__init__()
        self.dicKet = OrderedDict()
        self.keys = []
        self.setQuantumType = set()
        self._register_kets(kets)
        self._qval = None

    def _register_kets(self, kets):
        for ket in kets:
            # check nested ProductKet instance
            if isinstance(ket, ProductKet):
                for k, v in ket.dicKet.items():
                    self.dicKet[k] = v
                self.keys.extend(ket.keys)
                self.setQuantumType |= ket.setQuantumType
            else: # a pure ket
                key = ket.keys[0]
                self.dicKet[key] = ket
                self.keys.append(key)
                self.setQuantumType.add(ket.QUANTUM_TYPE)

    @property
    def qval(self):
        return tuple(self[key].qval for key in self.keys)

    @qval.setter
    def qval(self, val):
        self._qval = val

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dicKet[self.keys[key]]
        else:
            return self.dicKet[key]

    def __iter__(self):
        for key in self.keys:
            yield self.dicKet[key]

    def __deepcopy__(self, memo):
        '''The original deepcopy is well-equipped and slow.
        This method improves the speed of ket instance copying.'''

        cp_productket = type(self)() # instantiate newly
        memo[id(self)] = self # __deepcopy__ needs memo dictionary
        cp_productket.weight = self.weight # weight
        cp_productket.keys = self.keys # list of keys
        for k, ori_ket in self.dicKet.items():
            cp_ket = type(ori_ket)(**ori_ket.init_args)
            memo[id(ori_ket)] = ori_ket
            cp_ket.qval = ori_ket.qval # qval must be immutable
            cp_productket.dicKet[k] = cp_ket

        return cp_productket


class Bases(ProductKet):
    '''Bases are flock of basis (ket or product kets).'''

    QUANTUM_TYPE = 'QuantumBases'
    dicFilter =  {} # filter function against a specific ket

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
        
    def __init__(self, *iterKets):
        # hash table for searching index of specific ket
        self.dicKet = OrderedDict()
        self.dicIndex = {} # dic qval <-> index of ket
        self.tupKey = None # tuple for storing key of dicKet

        self.keys = []
        for iterKet in iterKets:
            if isinstance(iterKet, type(self)):
                self.keys.extend(iterKet.keys)
            else:
                key = iterKet.keys[0]
                self.keys.append(key)

        # Create index hash
        index = 0
        for i, multiKet in enumerate(itertools.product(*iterKets)):
            # product ket
            pket = ProductKet(*multiKet)
            
            # impose filter condition to the united ket
            flag = False
            for filterFunc in self.dicFilter.values():
                if not filterFunc(pket):
                    flag = True
                    break
            if flag:
                continue

            pket.keys = self.keys

            self.dicKet[pket.qval] = pket

            self.dicIndex[pket.qval] = index

            index += 1 # Caution: index != i when flag==True occurs even once.

        # tuple of keys of dicKet (OrderedDict)
        self.tupKey = tuple(self.dicKet)

        # size of bases
        self.N = len(self.dicKet)

    def get_index_from_ket(self, pket):
        '''Searching an index of a specific ket. Firstly, extract 
        the qval in each ket from a product ket as indKey.
        (eg.) (0, 0, 2, (1, 0, 0, 1))
        Then, search the index using dicKet.'''

        try:
            index = self.dicIndex[pket.qval]

        except KeyError:
            raise ValueError("ket {qval} doesn\'t exist".format(qval=pket.qval))

        return index

    def get_index_from_qval(self, qval):
        try:
            index = self.dicIndex[qval]

        except KeyError:
            raise ValueError("ket {qval} doesn\'t exist".format(qval=pket.qval))

        return index

    def __getitem__(self, key):
        '''Input type is integer. Return a product ket in accordance with
        the given index.'''

        if isinstance(key, int):
            return self.dicKet[self.tupKey[key]]
        elif isinstance(key, tuple):
            return self.dicKet[key]
        else:
            raise ValueError('Index must be interger.')

    def __iter__(self):
        self.cur = 0
        return self

    def __next__(self):
        if self.cur >= self.N:
            raise StopIteration

        pket = self.dicKet[self.tupKey[self.cur]]

        self.cur += 1

        return pket

    def __len__(self):
        return self.N


def show_ket(ket_or_iterKet):
    if isinstance(ket_or_iterKet, Ket):
        ket = ket_or_iterKet
        ket.show()
    else:
        for i, ket in enumerate(ket_or_iterKet, 1):
            print(i) 
            show_ket(ket) # recursive
