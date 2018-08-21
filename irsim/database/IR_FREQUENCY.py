from collections import namedtuple

Key = namedtuple('Key', 'mode modeNum')

# frequency for hamiltonian of IR
DIC_IR_FREQUENCY = {
        Key(mode='t1u', modeNum=4):0.00629777152672,
        Key(mode='gu', modeNum=5): 0.00607391422943,
        Key(mode='gu', modeNum=6): 0.00654888037462,
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

