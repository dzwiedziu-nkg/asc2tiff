import sys
import numpy as np


def process(file):
    ncols = 0
    nrows = 0
    xllcorner = 0
    yllcorner = 0
    dx = 0
    dy = 0

    with open(file) as f:
        ncols = int(f.readline().split()[1])
        nrows = int(f.readline().split()[1])
        xllcorner = float(f.readline().split()[1])
        yllcorner = float(f.readline().split()[1])
        dx = float(f.readline().split()[1])
        dy = float(f.readline().split()[1])

        arr = np.zeros((nrows, ncols))
        for r in range(0, nrows):
            line = f.readline().split()
            for c in range(0, ncols):
                arr[r, c] = line[c]

        arr[arr == -9999] = np.nan

    min_val = np.nanmin(arr)
    max_val = np.nanmax(arr)
    print(f'{file}: min_val={min_val}, max_val={max_val}')
    return min_val, max_val


if __name__ == "__main__":
    arr = []
    for arg in sys.argv[1:]:
        min_val, max_val = process(arg)
        arr.extend([min_val, max_val])
    min_ever = min(arr)
    max_ever = max(arr)
    print(f'min_ever={min_ever}, max_ever={max_ever}')
    print(f'So, please run:\n\npython convert.py {min_ever} {max_ever} ' + ' '.join(sys.argv[1:]))
