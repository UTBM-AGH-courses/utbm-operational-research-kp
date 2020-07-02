import random
import numpy as np
import random as rd
from random import randint
import matplotlib.pyplot as plt
import time


# La mutation consiste à inverser une valeur
def mutation(parents):
    mutants = np.zeros((parents.shape), dtype=int)
    taux_mutation = 0.5
    new_pop = parents
    for i in range(mutants.shape[0]):
        random_valeur = rd.random()
        mutants[i, :] = parents[i, :]
        if random_valeur > taux_mutation:
            continue
        nb_permute = 1
        for p in range(nb_permute):
            # Choisir l'index des valeurs à inverser
            index1 = randint(0, parents.shape[1]-1)
            index2 = randint(0, parents.shape[1]-1)
            # Permutation
            value1 = mutants[i, index1]
            value2 = mutants[i, index2]
            mutants[i, index1] = value2
            mutants[i, index2] = value1
    new_pop = np.vstack((new_pop, mutants))
    return new_pop


# Sélection des enfants
def croisement(parents, nbr_enfants):
    enfants = np.zeros((nbr_enfants, parents.shape[1]), dtype=int)
    new_pop = parents
    point_de_croisement = int(parents.shape[1]/2)  # croisement au milieu
    taux_de_croisement = 0.8
    i = 0
    # Tant qu'il y a des enfants
    while (i < nbr_enfants):
        indice_parent1 = i % parents.shape[0]
        indice_parent2 = (i+1) % parents.shape[0]
        x = rd.random()
        if x > taux_de_croisement:  # parents stériles
            continue
        enfants[i, 0:point_de_croisement] = parents[indice_parent1,
                                                    0:point_de_croisement]
        enfants[i, point_de_croisement:] = parents[indice_parent2,
                                                   point_de_croisement:]
        i += 1
    return enfants

# Sélection des parents à faire muter


def selection(fitness, nbr_parents, population, pop_size):
    fitness = list(fitness)
    parents = np.empty((nbr_parents, pop_size[1]), dtype=int)
    for i in range(nbr_parents):
        indice_max_fitness = np.where(fitness == np.max(fitness))
        parents[i] = population[indice_max_fitness[0][0]]
        fitness[indice_max_fitness[0][0]] = -999999
    return parents


# Calcul des distances de la population
def cal_distance(population, tableau_distances, pop_size):
    distances_pop = []
    for i in range(len(population)):
        eval_distance = 0
        for p in range(pop_size[0]):
            origine, destination = population[i][p], population[i][(
                p+1) % pop_size[1]]
            eval_distance += tableau_distances[origine][destination]
        distances_pop.append(eval_distance)
    return distances_pop

# Calcul de la fitness


def cal_fitness(distances_pop, pop_size):
    fitness_pop = []
    for p in range(pop_size[0]):
        fitness_pop.append(1/distances_pop[p])
    return fitness_pop

# Algo génétique


def optimize(tableau_distances, population, pop_size, nbr_generations):
    sol_opt, historique_fitness, historique_distance = [], [], []
    nbr_parents = pop_size[0]//2
    nbr_enfants = pop_size[0] - nbr_parents
    for i in range(nbr_generations):
        # OK -> Calcul des distances
        distances_pop = cal_distance(population, tableau_distances, pop_size)
        # OK -> Calcul de la fitness
        fitness = cal_fitness(distances_pop, pop_size)
        historique_fitness.append(fitness)
        # OK -> Sélection de ceux avec la meilleure fitness
        parents = selection(fitness, nbr_parents, population, pop_size)
        # OK -> On croise ceux avec la meilleur fitess
        # enfants = croisement(parents, nbr_enfants)
        parents = mutation(parents)
        population[0:parents.shape[0]] = parents
        historique_distance.append(
            np.min(cal_distance(population, tableau_distances, pop_size)))
    print('Voici la dernière génération de la population: \n{}\n'.format(population))
    fitness_derniere_generation = cal_fitness(distances_pop, pop_size)
    print('Fitness de la dernière génération: \n{}\n'.format(
        fitness_derniere_generation))
    max_fitness = np.where(fitness_derniere_generation ==
                           np.max(fitness_derniere_generation))
    sol_opt = population[max_fitness[0][0]:]
    min_distance = np.min(cal_distance(sol_opt, tableau_distances, pop_size))
    return sol_opt, historique_fitness, historique_distance, min_distance

# Génération des distances


def gen_distances(nb_villes):
    distances = np.zeros((nb_villes, nb_villes))
    for ville in range(nb_villes):
        villes = [i for i in range(nb_villes) if not i == ville]
        for vers_la_ville in villes:
            distances[ville][vers_la_ville] = random.randint(50, 2000)
            distances[vers_la_ville][ville] = distances[ville][vers_la_ville]
    return distances


start_time = time.time()
NB_VILLES = 10
tableau_distances = gen_distances(NB_VILLES)
print('Voici la matrice des distances entres les villes \n', tableau_distances)

population = []
pop_size = (6, NB_VILLES)
nbr_generations = 1000

for i in range(pop_size[0]):
    population.append(random.sample(range(NB_VILLES), NB_VILLES))

sol_opt, historique_fitness, historique_distance, min_distance = optimize(
    tableau_distances, population, pop_size, nbr_generations)

# Affichage du résultat
print('La solution optimale est: \n{}'.format(sol_opt))
print(np.asarray(historique_fitness).shape)
print('Avec une valeur de : ', min_distance, 'km')

print("--- Temps d'éxécution : %ss ---" % (time.time() - start_time))


# Plot
historique_fitness_moyenne = [np.mean(fitness)
                              for fitness in historique_fitness]
historique_fitness_max = [np.max(fitness) for fitness in historique_fitness]

x = list(range(nbr_generations))
y1 = historique_fitness_moyenne
y2 = historique_fitness_max
y3 = historique_distance

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Génerations')

ax1.set_ylabel('Fitness')
ax1.plot(x, y1, label='Valeurs moyennes')
ax1.plot(x, y2, label='Valeurs maximale')
ax1.tick_params(axis='y')

ax2 = ax1.twinx()  
ax2.set_ylabel('Distance')
ax2.plot(x, y3, color='red', label='Distance')
ax2.tick_params(axis='y')

fig.tight_layout()
plt.show()
