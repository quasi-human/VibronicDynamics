from collections import namedtuple
import inspect
import os
from .CONSTANT import MILLI_EV2AU


Key = namedtuple('Key', 'Alpha J P')


def import_vibronic_energy_levels(path):
    # import data
    with open(path, 'r') as f:
        lines = f.readlines()

    dicVEL = {} # dictionary vibronic energy levels

    cur = 'label'
    for line in lines:
        line = line[:-1]
        if line[0] == '#':
            continue

        if cur == 'label':
            J, P = map(int, line.split())

            cur = 'data' # update current cursor

        else:
            genEigenEnergy = (MILLI_EV2AU * float(e) for e in line.split('\t'))

            for i, e in enumerate(genEigenEnergy, 1):
                Alpha = i
                dicVEL[Key(Alpha=Alpha, J=J, P=P)] = e

            cur = 'label' # update current cursor

    return dicVEL

# get this file path (absolute path to the directory which contains this file.)
THIS_FILE_PATH = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))
path = os.path.join(THIS_FILE_PATH + 'Vibronic_energy_levels.dat')

if __name__ == '__main__':
    #path = r'/home/yuki/jte/database/Vibronic_energy_levels.dat'
    #path = r'./Vibronic_energy_levels.dat'
    path = r'/home/yuki/jte/irsim/database/Vibronic_energy_levels.dat'
    dicVEL = import_vibronic_energy_levels(path)

    l = []
    for k, v in dicVEL.items():
        l.append((k, v))
        print(k)
        print(v/MILLI_EV2AU) 

    l = sorted(l, key=lambda e: e[1], reverse=True)
    for key, val in l:
        print(key, val)

    diff = l[-2][1] - l[-1][1]
    print(diff * 27 / 8.617303e-5)
    print(diff * 27)

    #print(dicVEL[(1,1,1)])

