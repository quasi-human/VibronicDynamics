# Functions for writing pretty code

def _generate_line(lines):
    lis = lines.split('\n')
    for line in lis:
        yield line

def _get_max_space(txt):
    bgn = txt.find('[')
    end = txt.find(']')

    txt = txt[bgn + 1: end]
    #txt.replace(' ', '')
    l = txt.split(',')

    ll = []
    for e in l:
        e = _truncate_head_object(e, ' ')
        ll.append(len(e))
    return max(ll)

def _truncate_head_object(txt, obj=' '):
    while True:
        if txt[0] == obj:
            txt = txt[1:]
        else:
            break
    return txt


    
def _give_space(txt, val):
    bgn = txt.find('[')
    end = txt.find(']')

    front = txt[: bgn + 1]
    back = txt[end:]

    txt = txt[bgn + 1: end]
    #txt.replace(' ', '')
    l = txt.split(',')

    it = map(_truncate_head_object, l)
    filled = [' ' * (val - len(e) + 1) + e for e in it]

    item = ','.join(filled)

    ret = front + item + back

    return ret

def _pretty_mtrx(stack):
    max_ = 0
    for line in stack:
        lMax = _get_max_space(line)
        max_ = max(max_, lMax)

    #ret = [_give_space(e) for e in stack]
    for e in stack:
        yield _give_space(e, max_)

    #return ret

    
     
def pretty_mtrx(lines):
    stack = []
    for line in _generate_line(lines):
        if '[' in line and ']' in line:
            stack.append(line)
            continue
        else:
            if stack:
                for item in _pretty_mtrx(stack):
                    print(item)
            print(line)
            stack = []

txt = '''
        Key('hg', 't1', 'h', 1): {
            'theta': (1/4) * sqrt(1/6) * np.array([
                    [ 110, 0, 0, 0, 0],
                    [ 0, 12220, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),
                    }
        '''

pretty_mtrx(txt)



#TEMPLATE
'''
        Key('hg', 't1', 'h', 1): {
            'theta': (1/4) * sqrt(1/6) * np.array([
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),

            'epsilon': (1/4) * sqrt(1/6) * np.array([
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),

            'xi': (1/4) * sqrt(1/6) * np.array([
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),

            'eta': (1/4) * sqrt(1/6) * np.array([
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),

            'zeta': (1/4) * sqrt(1/6) * np.array([
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0]]),
            },
            '''
