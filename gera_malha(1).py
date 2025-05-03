import sys
import numpy as np

def ler_mapa(arquivo):
    return np.loadtxt(arquivo)

def circulo_completo_em_area_a(cx, cy, R, mapa):
    """
    Verifica se TODO o círculo de raio R ao redor de (cx, cy) está dentro da Área A (valor == 1)
    """
    max_x, max_y = mapa.shape
    for dx in range(-int(R), int(R) + 1):
        for dy in range(-int(R), int(R) + 1):
            if dx**2 + dy**2 <= R**2:
                nx = int(round(cx + dx))
                ny = int(round(cy + dy))
                if (0 <= nx < max_x) and (0 <= ny < max_y):
                    if mapa[nx, ny] != 1:
                        return False
                else:
                    return False  # Saiu do mapa
    return True

def gerar_malha(x1, y1, x2, y2, R, mapa):
    """
    Gera uma malha de círculos com distância constante R*sqrt(3) entre si,
    apenas em pontos válidos da Área A.

    Args:
        x1, y1, x2, y2: coordenadas dos dois primeiros círculos.
        R: raio do círculo.
        mapa: matriz numpy carregada.

    Returns:
        Lista de coordenadas [(x, y), ...]
    """
    coords = []
    max_x, max_y = mapa.shape

    # Vetor base (direção da linha principal)
    dx = x2 - x1
    dy = y2 - y1
    distancia_base = np.sqrt(dx**2 + dy**2)

    if distancia_base == 0:
        print("Erro: (x1, y1) e (x2, y2) não podem ser iguais.")
        return []

    # Unidade do vetor base
    ux = dx / distancia_base
    uy = dy / distancia_base

    # Vetor perpendicular (para deslocar linhas)
    perp_ux = -uy
    perp_uy = ux

    # Distâncias importantes
    dist_entre_circulos = R * np.sqrt(3)
    dist_entre_linhas = (3 / 2) * R
    fase = 0.5 * R * np.sqrt(3)

    # Determinar faixa suficiente para cobrir toda a área do mapa
    linha_min = -int((max_x + max_y) / dist_entre_linhas) - 1
    linha_max = int((max_x + max_y) / dist_entre_linhas) + 1
    coluna_min = -int((max_x + max_y) / dist_entre_circulos) - 1
    coluna_max = int((max_x + max_y) / dist_entre_circulos) + 1

    for linha in range(linha_min, linha_max):
        # Deslocamento perpendicular
        offset_x = linha * dist_entre_linhas * perp_ux
        offset_y = linha * dist_entre_linhas * perp_uy

        # Fase alternada para linhas ímpares
        fase_offset = (abs(linha) % 2) * fase

        for coluna in range(coluna_min, coluna_max):
            desloc_x = (coluna * dist_entre_circulos + fase_offset) * ux
            desloc_y = (coluna * dist_entre_circulos + fase_offset) * uy

            cx = x1 + desloc_x + offset_x
            cy = y1 + desloc_y + offset_y

            cx_int = int(round(cx))
            cy_int = int(round(cy))

            # Checa se está dentro do mapa e se o círculo completo cabe na Área A
            if (0 <= cx_int < max_x) and (0 <= cy_int < max_y):
                if circulo_completo_em_area_a(cx, cy, R, mapa):
                    coords.append((cx_int, cy_int))

    return coords

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Uso: python gera_malha.py <arquivo_mapa> <x1> <y1> <x2> <y2> <R>")
        sys.exit(1)

    arquivo_mapa = sys.argv[1]
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])
    R = float(sys.argv[6])

    mapa = ler_mapa(arquivo_mapa)

    malha = gerar_malha(x1, y1, x2, y2, R, mapa)

    if not malha:
        print("Nenhuma coordenada válida encontrada para a malha.")
    else:
        for c in malha:
            print(f"{c[0]} {c[1]}")

