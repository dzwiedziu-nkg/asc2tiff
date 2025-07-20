import sys

import numpy as np
import png
import trimesh

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

    # 3) Wygeneruj współrzędne X,Y
    xs = np.linspace(0, dx*(W-1), W, dtype=np.float32)
    ys = np.linspace(0, dy*(H-1), H, dtype=np.float32)
    xv, yv = np.meshgrid(xs, ys)

    # 4) Wierzchołki: spłaszczone (x, y, z)
    vertices = np.column_stack((xv.ravel(), yv.ravel(), height.ravel()))

    # 5) Faces: dla każdej „komórki” (i,j) dwa trójkąty
    faces = []
    for i in range(H-1):
        for j in range(W-1):
            idx = i*W + j
            # trójkąt 1
            faces.append([idx, idx+1, idx+W])
            # trójkąt 2
            faces.append([idx+1, idx+W+1, idx+W])
    faces = np.array(faces, dtype=np.int64)

    # 6) Zbuduj siatkę
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    return mesh

if __name__ == "__main__":
    # ścieżki i skale możesz dostosować do swoich danych:
    png_path = sys.argv[1]
    mesh = heightmap_to_mesh(png_path, dx=1.0, dy=1.0, dz=0.05)

    # zapisz do OBJ i STL
    mesh.export("terrain.obj")
    mesh.export("terrain.stl")
    print("Zapisano terrain.obj i terrain.stl")
