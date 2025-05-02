import sys
import numpy as np
import random

def ler_mapa(arquivo):
    return np.loadtxt(arquivo)

def encontrar_area_a(matriz):
    # Considerando que Área A é representada por 1 e Área B por 0
    coords = np.argwhere(matriz == 1)
    return [tuple(coord) for coord in coords]

def distancia(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def selecionar_coordenada_completa(area_a, matriz, R):
    """
    Seleciona uma coordenada aleatória da Área A (p1), mas apenas aceita se
    TODOS os pontos a ~R*sqrt(3) de distância também pertencerem à Área A.
    Retorna p1 se encontrar, ou None se não encontrar após várias tentativas.
    """
    area_a_set = set(area_a)
    tentativas = 10000  # Evita loop infinito
    tolerancia = 0.5  # Um pouco mais flexível para encontrar distâncias discretas
    distancia_alvo = R * np.sqrt(3)
    max_offset = int(np.ceil(distancia_alvo)) + 1  # Raio máximo de busca

    for _ in range(tentativas):
        p1 = random.choice(area_a)
        x1, y1 = p1
        completo = True

        # Procurar por pontos exatamente a distancia_alvo
        for dx in range(-max_offset, max_offset + 1):
            for dy in range(-max_offset, max_offset + 1):
                x2, y2 = x1 + dx, y1 + dy
                if (0 <= x2 < matriz.shape[0]) and (0 <= y2 < matriz.shape[1]):
                    d = distancia(p1, (x2, y2))
                    # Só nos interessam os pontos a ~R*sqrt(3)
                    if np.isclose(d, distancia_alvo, atol=tolerancia):
                        if (x2, y2) not in area_a_set:
                            completo = False
                            break
            if not completo:
                break

        if completo:
            return p1  # Encontrou coordenada válida

    return None  # Não encontrou coordenada válida

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python coordenada1.py <arquivo_mapa> <raio>")
        sys.exit(1)

    arquivo_mapa = sys.argv[1]
    R = float(sys.argv[2])

    matriz = ler_mapa(arquivo_mapa)
    area_a = encontrar_area_a(matriz)

    if not area_a:
        print("None")
    else:
        coordenada = selecionar_coordenada_completa(area_a, matriz, R)
        if coordenada:
            print(f"{coordenada[0]} {coordenada[1]}")
        else:
            print("None")
