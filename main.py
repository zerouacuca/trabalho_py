# main.py
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
from gera_malha import gerar_malha

def ler_mapa(caminho):
    return np.loadtxt(caminho)

if __name__ == "__main__":
    mapa_path = "mapa.dat"
    R = 50

    ##if len(sys.argv) != 3:
    ##      print("Uso: python main.py <mapa.txt> <R>")
    ##        sys.exit(1)

    ##mapa_path = sys.argv[1]
    ##R = float(sys.argv[2])
    mapa = ler_mapa(mapa_path)

    # Executa seeds.py e lê coordenadas
    saida = subprocess.check_output(["python", "seeds.py", str(R)], text=True)
    linhas = saida.strip().splitlines()

    x1, y1 = map(float, linhas[0].split())  # Coordenada 1 (translacao)
    x2, y2 = map(float, linhas[1].split())  # Coordenada 2
    angulo = float(linhas[2])              # Angulo em radianos

    coords_malha = gerar_malha(x1, y1, x2, y2, R, mapa)

    # Agora todas as variaveis estao armazenadas em memoria:
    # x1, y1, angulo, coords_malha

    # Plotagem
    fig, ax = plt.subplots()
    ax.imshow(mapa.T, origin='lower', cmap='gray')
    ax.set_title("Mapa com malha de círculos")
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")

    for cx, cy in coords_malha:
        ax.add_patch(plt.Circle((cx, cy), R, fill=False, edgecolor='blue'))
        ax.plot(cx, cy, 'b.', markersize=3)

    ax.plot(x1, y1, 'go')
    ax.add_patch(plt.Circle((x1, y1), R, fill=False, linestyle='--', edgecolor='green', linewidth=1.5, label="Círculo 1 (fixo)"))

    ax.plot(x2, y2, 'ro')
    ax.add_patch(plt.Circle((x2, y2), R, fill=False, linestyle='--', edgecolor='red', linewidth=1.5, label="Círculo 2 (ângulo)"))

    ax.legend(loc='upper right')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
