import sys
import numpy as np
import matplotlib.pyplot as plt

def ler_mapa(arquivo):
    return np.loadtxt(arquivo)

def desenhar_malha_hexagonal(mapa, coordenada1, coordenada2, raio):
    """
    Gera uma malha hexagonal de círculos no mapa com base nas coordenadas e raio fornecidos.
    """
    print(f"Desenhando malha hexagonal com coordenadas {coordenada1} e {coordenada2} e raio {raio}")

    fig, ax = plt.subplots()
    ax.imshow(mapa, cmap='gray')

    # Aqui vamos desenhar círculos com a distância de R * sqrt(3)
    altura, largura = mapa.shape
    dx = int(np.round(raio * np.sqrt(3)))

    for y in range(0, altura, dx):
        for x in range(0, largura, dx):
            ax.add_patch(plt.Circle((x, y), raio, color='red', fill=False))

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: python malha_hex.py <arquivo_mapa> <raio> <coordenada1_x> <coordenada1_y> <coordenada2_x> <coordenada2_y>")
        sys.exit(1)

    arquivo_mapa = sys.argv[1]
    R = float(sys.argv[2])
    coordenada1 = (int(sys.argv[3]), int(sys.argv[4]))
    coordenada2 = (int(sys.argv[5]), int(sys.argv[6]))

    print(f"Arquivo do mapa: {arquivo_mapa}")
    print(f"Raio: {R}")
    print(f"Coordenada 1: {coordenada1}")
    print(f"Coordenada 2: {coordenada2}")

    # Leitura do mapa
    mapa = ler_mapa(arquivo_mapa)

    # Desenho da malha hexagonal
    desenhar_malha_hexagonal(mapa, coordenada1, coordenada2, R)
