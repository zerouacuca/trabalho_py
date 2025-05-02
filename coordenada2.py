import sys
import numpy as np

def select_escape_coordinate(center, R, seed=None):
    """
    Seleciona uma coordenada a exatamente R * sqrt(3) de distância do centro,
    com ângulo aleatório entre 0 e pi.
    """
    if seed is not None:
        np.random.seed(seed)

    D = R * np.sqrt(3)
    x0, y0 = center

    angle = np.random.uniform(0, np.pi)

    x1 = x0 + D * np.cos(angle)
    y1 = y0 + D * np.sin(angle)

    new_point = (int(round(x1)), int(round(y1)))
    return new_point

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python coordenada2.py <x> <y> <raio>")
        sys.exit(1)

    x = int(sys.argv[1])
    y = int(sys.argv[2])
    R = float(sys.argv[3])
    center = (x, y)

    seed = x + y  # Opcional: usa a soma como semente

    new_coord = select_escape_coordinate(center, R, seed=seed)
    print(f"{new_coord[0]} {new_coord[1]}")
