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

    # Marcar os centros
    plt.plot(y1, x1, 'bo')  # Centro 1
    plt.plot(y2, x2, 'ro')  # Centro 2

    plt.legend()
    plt.title("Mapa com dois círculos")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.show()

if __name__ == "__main__":
    main()