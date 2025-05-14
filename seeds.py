import sys
import numpy as np

def gerar_sementes(R):
    # Semente 1: dentro de um círculo de raio R no primeiro quadrante
    while True:
        x = np.random.uniform(0, R)
        y = np.random.uniform(0, R)
        if x**2 + y**2 <= R**2:
            break

    x1, y1 = x, y

    # Semente 2: a uma distância fixa (R * sqrt(3)) com ângulo entre 0 e pi/2
    angulo = np.random.uniform(0, np.pi / 2)
    distancia = R * np.sqrt(3)
    x2 = x1 + distancia * np.cos(angulo)
    y2 = y1 + distancia * np.sin(angulo)

    return (x1, y1), (x2, y2), angulo

if __name__ == "__main__":
    R = float(sys.argv[1])
    semente1, semente2, angulo = gerar_sementes(R)

    print(f"{semente1[0]} {semente1[1]}")
    print(f"{semente2[0]} {semente2[1]}")
    print(f"{angulo}")
