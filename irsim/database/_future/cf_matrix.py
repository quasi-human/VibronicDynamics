class JT_COUPLING_CONSTANT:
    def __init__(self, fromState, toState, mtrx):
        self.fromState = fromState
        self.toState = toState
        self.mtrx = mtrx


DIC_JT_CF = {
        (1, 2, -1): {
            (1, 2, -1): {
                'mtrx': 
                [[-1/10, 0, 0, 0, -1/2],
                 [0, 2/5, 0, 0, 0],
                 [0, 0, -3/5, 0, 0],
                 [0, 0, 0, 2/5, 0],
                 [-1/2, 0, 0, 0, -1/10]],
                'XI': 0.26736
                }
            }
        }


DC_CF_CONSTANT = {
        ('t1u3', '2H'): 0,
        }



            
if __name__ == '__main__':
    mtrx = [[-1/10, 0, 0, 0, -1/2],
            [0, 2/5, 0, 0, 0],
            [0, 0, -3/5, 0, 0],
            [0, 0, 0, 2/5, 0],
            [-1/2, 0, 0, 0, -1/10]]

    CF22n1 = JT_COUPLING_CONSTANT((1, 2, -1), (1, 2, -1), mtrx)

    print(CF22n1.mtrx)
    




