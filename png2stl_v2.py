import sys

import numpy as np
import png
from pydelatin import Delatin                   # pydelatin → szybkie triangulowanie wysokości :contentReference[oaicite:0]{index=0}
import meshio


def read_16bit_gray_alpha(png_path):
    reader = png.Reader(png_path)
    width, height, rows, info = reader.read()
    bitdepth = info['bitdepth']      # powinno być 16
    planes   = info['planes']        # 2 (gray + alpha)
    if bitdepth != 16 or (planes != 2 and planes != 1):
        raise ValueError("To nie jest 16‑bitowy grayscale+alpha PNG")

    # każda linia to sekwencja 16‑bitowych słów: [G, A, G, A, ...]
    # zbieramy do tablicy uint16
    data = np.vstack([np.fromiter(row, dtype=np.uint16) for row in rows])
    data = data.reshape((height, width, planes))
    gray = data[:, :, 0]
    alpha = data[:, :, 1] if planes == 2 else None
    return gray, alpha

def heightmap_to_mesh(png_path, dx=1.0, dy=1.0, dz=0.1):
    height, apha = read_16bit_gray_alpha(png_path)
    H, W = height.shape

    tin = Delatin(height,
                  height=H, width=W,
                  z_scale=0.001,  # skalowanie Z względem X/Y
                  z_exag=1.0,  # egzaggeacja
                  max_error=10)
    verts = tin.vertices  # (N, 3)
    triangles = tin.triangles  # (M, 3)



    # 6) Zapis do OBJ i STL przez meshio
    mesh = meshio.Mesh(points=verts,
                       cells=[("triangle", triangles)])
    mesh.write('terrain22.obj')
    # mesh.write('terrain22.stl')

if __name__ == "__main__":
    # ścieżki i skale możesz dostosować do swoich danych:
    png_path = sys.argv[1]
    heightmap_to_mesh(png_path, dx=1.0, dy=1.0, dz=0.05)
