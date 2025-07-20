import sys
import png

import numpy as np
from PIL import Image


def save_16bit_png_with_alpha(arr, out_filename, min_level, max_level):
    # 1) Załóżmy, że arr to 2D numpy float z nan tam, gdzie brak danych.
    mask = np.isnan(arr)

    # 2) Wyodrębnij tylko wartości ważne, policz min/max:
    valid = ~mask
    minv = min_level
    maxv = max_level

    # 3) Przeskaluj wszystkie wartości do [0, 65535]
    scale = 65535.0 / (maxv - minv)
    arr16 = np.zeros_like(arr, dtype=np.uint16)
    arr16[valid] = np.round((arr[valid] - minv) * scale).astype(np.uint16)
    # pozostałe (nan) zostaną 0 – ale i tak będą całkowicie przezroczyste

    # 4) Stwórz alfa‑kanał 16‑bit: 0 tam, gdzie mask==True, 65535 tam, gdzie dane
    alpha = np.zeros_like(arr16)
    alpha[valid] = 65535

    height, width = arr16.shape

    # 5) Zapisz PNG: tryb grayscale + alpha, 16 bit
    with open(out_filename, 'wb') as f:
        writer = png.Writer(
            width=width,
            height=height,
            bitdepth=16,
            greyscale=True,
            alpha=True
        )

        def row_iter():
            for y in range(height):
                # każdy wiersz to [p, a, p, a, p, a, ...]
                row = np.empty((width * 2,), dtype=np.uint16)
                row[0::2] = arr16[y]
                row[1::2] = alpha[y]
                yield row.tolist()

        writer.write(f, row_iter())

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
    return arr


if __name__ == "__main__":
    for file in sys.argv[3:]:
        arr = process(file)
        out_filename = file.replace('.asc', '.png')
        if not out_filename.endswith('.png'):
            out_filename = out_filename + '.png'

        save_16bit_png_with_alpha(arr, out_filename, float(sys.argv[1]), float(sys.argv[2]))
        print(f'Saved to {out_filename}')
