import networkx as nx
import numpy as np
from mealpy import FloatVar
from mealpy import GA
import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Tworzenie grafu i budowa list krawędzi
# ---------------------------------------------------------
def create_random_graph(n, p):
    G = nx.fast_gnp_random_graph(n, p, seed=40, directed=True)
    return G
N = 150

prob = 0.7
G = create_random_graph(N, prob)
edges = list(G.edges()) #lista krawędzi - wszystkie mozlliwe polaczaczenia
E = len(edges) #liczba krawedzi
edge_to_idx = {e: i for i, e in enumerate(edges)} #mapa krawedz -> indeks w wektorze wag

# ---------------------------------------------------------
# 2. Generowanie flows
# ---------------------------------------------------------
def generate_flows(G, K):
    """Zwraca listę K losowych flowów (s,d,intensity), s!=d"""
    np.random.seed(173223)
    nodes = list(G.nodes())
    flows = set()

    while len(flows) < K:
        s, d = np.random.choice(nodes, 2, replace=False)
        intensity = np.random.randint(1, 10)   # losowa intensywność 1–9
        flows.add((s, d, intensity))

    return list(flows)

K = 300   # liczba flowów
flows = generate_flows(G, K)

# ---------------------------------------------------------
# Funkcja - Load Vector L
# ---------------------------------------------------------
def compute_load(weights, flows):
    """Przyjmuje wektor wag krawędzi i zwraca wektor obciążeń L z uwzględnieniem intensywności flowów"""
    for (e, w) in zip(edges, weights):
        G[e[0]][e[1]]["weight"] = w

    load = np.zeros(E)

    for (s, d, intensity) in flows:
        try:
            path = nx.shortest_path(G, source=s, target=d, weight="weight")
        except nx.NetworkXNoPath:
            continue

        for i in range(len(path) - 1):
            e = (path[i], path[i+1])
            idx = edge_to_idx[e]
            load[idx] += intensity   # zamiast +1 dodajemy natężenie flowu

    return load



# ---------------------------------------------------------
# 3. Funkcja fitness = max load
# ---------------------------------------------------------
def evaluate_fitness(weights):
    load = compute_load(weights, flows)
    return np.max(load)


# ---------------------------------------------------------
# 4. Definiowanie problemu GA
# ---------------------------------------------------------
problem = {
    "bounds": FloatVar(lb=(1,) * E, ub=(100,) * E, name="weights"),
    "obj_func": evaluate_fitness,
    "minmax": "min",
}

# ---------------------------------------------------------
# 5. Uruchomienie algorytmu GA
# ---------------------------------------------------------
model = GA.BaseGA(
    problem=problem,
    epoch=100,
    pop_size=100,
    pc=0.9,
    pm=0.05
)

start = time.time()
g_best = model.solve(problem)
end = time.time()

total_time = end - start

# ---------------------------------------------------------
# 6. Dodatkowe statystyki
# ---------------------------------------------------------
best_weights = g_best.solution
load_vector = compute_load(best_weights, flows)
max_load = np.max(load_vector)
avg_load = np.mean(load_vector)
std_load = np.std(load_vector)

# ---------------------------------------------------------
# 7. Wyniki
# ---------------------------------------------------------
print(f"Total time: {total_time:.4f} seconds")
print("Best solution (weights):", best_weights)
print("Max load (Fitness):", g_best.target.fitness)
print("Average load:", avg_load)
print("STD load:", std_load)
print("Load vector L:", load_vector)
