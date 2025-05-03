import subprocess
import matplotlib.pyplot as plt
import numpy as np

def main():
    mapa_arquivo = 'mapa.dat'

    # Pergunta o valor do raio
    R = float(input("Digite o raio do círculo (em unidades do mapa): "))

    # Executa coordenada1.py
    print("Executando coordenada1.py...")
    resultado1 = subprocess.run(
        ['python', 'coordenada1.py', mapa_arquivo, str(R)],
        capture_output=True, text=True
    )
    saida1 = resultado1.stdout.strip()

    if saida1 == "None":
        print("Nenhuma coordenada válida encontrada pela coordenada1.py.")
        return

    print(f"Coordenada1 recebida: {saida1}")
    x1, y1 = map(int, saida1.split())

    # Executa coordenada2.py
    print("Executando coordenada2.py...")
    resultado2 = subprocess.run(
        ['python', 'coordenada2.py', str(x1), str(y1), str(R)],
        capture_output=True, text=True
    )
    saida2 = resultado2.stdout.strip()
    x2, y2 = map(int, saida2.split())
    print(f"Coordenada2 recebida: {saida2}")

    # Executa gera_malha.py
    print("Executando gera_malha.py...")
    resultado_malha = subprocess.run(
        ['python', 'gera_malha.py', mapa_arquivo, str(x1), str(y1), str(x2), str(y2), str(R)],
        capture_output=True, text=True
    )
    saida_malha = resultado_malha.stdout.strip()
    malha_coords = []
    if saida_malha:
        for linha in saida_malha.splitlines():
            parts = linha.strip().split()
            if len(parts) == 2:
                xi, yi = map(int, parts)
                malha_coords.append((xi, yi))
    print(f"{len(malha_coords)} círculos adicionais foram gerados.")

    # Carrega o mapa e plota
    mapa = np.loadtxt(mapa_arquivo)
    plt.figure(figsize=(8, 8))
    plt.imshow(mapa, cmap='gray', origin='lower')

    # Plota o primeiro círculo
    circle1 = plt.Circle((y1, x1), R, color='blue', fill=False, linewidth=2, label='Círculo 1')
    plt.gca().add_patch(circle1)

    # Plota o segundo círculo
    circle2 = plt.Circle((y2, x2), R, color='red', fill=False, linewidth=2, label='Círculo 2')
    plt.gca().add_patch(circle2)

    # Marcar os centros dos dois primeiros
    plt.plot(y1, x1, 'bo')  # Centro 1
    plt.plot(y2, x2, 'ro')  # Centro 2

    # Plota os círculos adicionais
    for xi, yi in malha_coords:
        circle_extra = plt.Circle((yi, xi), R, color='green', fill=False, linewidth=1)
        plt.gca().add_patch(circle_extra)
        plt.plot(yi, xi, 'go', markersize=3)  # Marca o centro pequeno

    plt.legend()
    plt.title("Mapa com malha de círculos")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.show()

if __name__ == "__main__":
    main()
