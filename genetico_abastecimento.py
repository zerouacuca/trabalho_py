import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from deap import base, creator, tools, algorithms
import random

RAIO = 50  # km
TAM_POP = 60
NUM_GERACOES = 60
NUM_PONTOS = 31  
CAMINHO_MAPA = "mapa.dat"

def carregar_mapa(filepath):
    return np.loadtxt(filepath)

def extrair_coordenadas_validas(mapa):
    return np.argwhere(mapa == 1)


def cobre_ponto(ponto_base, pontos, raio=RAIO):
    distancias = np.linalg.norm(pontos - ponto_base, axis=1)
    return pontos[distancias <= raio]


def cobertura_total(pontos_de_abastecimento, pontos_mapa, raio=RAIO):
    cobertos = set()
    for p in pontos_de_abastecimento:
        cobertos.update(map(tuple, cobre_ponto(np.array(p), pontos_mapa, raio)))
    return len(cobertos) / len(pontos_mapa)


def distancia_rota(pontos):
    dist = 0
    for i in range(len(pontos)):
        dist += euclidean(pontos[i], pontos[(i + 1) % len(pontos)])
    return dist


def fitness(individuo, pontos_mapa):
    pontos = [(individuo[i], individuo[i+1]) for i in range(0, len(individuo), 2)]
    cobertura = cobertura_total(pontos, pontos_mapa)
    rota_dist = distancia_rota(pontos)
    penalidade = 1000 * (1 - cobertura) if cobertura < 1 else 0
    return len(pontos) + rota_dist + penalidade,


def plotar_solucao(mapa, melhor_ind):
    pontos = [(melhor_ind[i], melhor_ind[i+1]) for i in range(0, len(melhor_ind), 2)]
    plt.imshow(mapa, cmap='gray')
    for (x, y) in pontos:
        circle = plt.Circle((y, x), RAIO, color='red', fill=False)
        plt.gca().add_patch(circle)
        plt.plot(y, x, 'ro')
    for i in range(len(pontos)):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        plt.plot([y1, y2], [x1, x2], 'b--')

    plt.title("Melhor Solução - Cobertura e Rota")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def mutar_com_limite(ind, mapa_shape, indpb=0.3):
    for i in range(len(ind)):
        if random.random() < indpb:
            if i % 2 == 0:
                ind[i] = random.randint(0, mapa_shape[0] - 1)  # x
            else:
                ind[i] = random.randint(0, mapa_shape[1] - 1)  # y
    return ind,


mapa = carregar_mapa(CAMINHO_MAPA) 
pontos_mapa = extrair_coordenadas_validas(mapa) 

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_int_x", lambda: random.randint(0, mapa.shape[0] - 1))
toolbox.register("attr_int_y", lambda: random.randint(0, mapa.shape[1] - 1))

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_int_x, toolbox.attr_int_y), n=NUM_PONTOS)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness, pontos_mapa=pontos_mapa)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutar_com_limite, mapa_shape=mapa.shape, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)


pop = toolbox.population(n=TAM_POP)
hof = tools.HallOfFame(1)

algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=NUM_GERACOES,
                    stats=None, halloffame=hof, verbose=True)


melhor_ind = hof[0]
print("Melhor indivíduo:", melhor_ind)
plotar_solucao(mapa, melhor_ind)