import numpy as np

# get effective digit in integer part
def get_integer_digit(*vals):
    vals = [np.abs(val) for val in vals]
    maxval = np.max(vals)
    if maxval == 0:
        return 0
    return int(np.log10(maxval) + 1)
