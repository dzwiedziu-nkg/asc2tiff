import numpy as np
from PIL import Image

file = 'result.asc'

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

print(arr.max() - arr.min())

arr2 = arr - arr.min()
arr3 = np.rint(arr2 * (1 / arr2.max() * (256*256-1)))
arr4 = arr3.astype(int)
im = Image.fromarray(arr4)
im.save("your_file.png")

