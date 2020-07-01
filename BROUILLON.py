# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 12:33:44 2020

@author: aabbas-t
"""
# Résolution du problème du sac à dos ou KP (Knapsack Problem) à l'aide d'algorithme génétique
# import de la librairie

import numpy as np #utilisation des calculs matriciels
#import pandas as pd #générer les fichiers csv
import random as rd #génération de nombre aléatoire
from random import randint # génération des nombres aléatoires  
import matplotlib.pyplot as plt


# Données du problème (générées aléatoirement)
nombre_objets = 30
capacite_max = 30       # La capacité du sac 
nbr_generations = 100   # Nombre de générations

ID_objets = np.arange(1, nombre_objets + 1) #ID des objets à mettre dans le sac de 1 à 10
poids = np.random.randint(1, 15, size=nombre_objets) # Poids des objets générés aléatoirement
valeur = np.random.randint(50, 350, size=nombre_objets) # Valeurs des objets générées aléatoirement

print('La liste des objet est la suivante :')
print('ID_objet   Poids   Valeur')
for i in range(ID_objets.shape[0]):
    print(f'{ID_objets[i]} \t {poids[i]} \t {valeur[i]}')
print()

def generer_tableau(population, poids, capacite_max):
    tableau = []
    for i in range(population[0]):
        row = np.random.randint(2, size = pop_size[1])
        mult = np.multiply(row,poids)
        while(np.sum(mult) > capacite_max):
            row = np.random.randint(2, size = pop_size[1])
            mult = np.multiply(row,poids)
        print('ligne ', i, ' OK')
        tableau.append(row.tolist())
    return np.array(tableau, dtype=np.int)


# Créer la population initiale
population = 8 # La taille de la population 
pop_size = (population, ID_objets.shape[0])
#population_initiale = np.random.randint(2, size = pop_size)
population_initiale = generer_tableau(pop_size, poids, capacite_max)
population_initiale = population_initiale.astype(int)

print('Taille de la population = {}'.format(pop_size))
print('Population Initiale: \n{}'.format(population_initiale))

    

def cal_fitness(poids, valeur, population, capacite):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * valeur)
        S2 = np.sum(population[i] * poids)
        if S2 <= capacite:
            fitness[i] = S1
        else :
            fitness[i] = 0 
    return fitness.astype(int)  

def selection(fitness, nbr_parents, population):
    fitness = list(fitness)
    parents = np.empty((nbr_parents, population.shape[1]))
    for i in range(nbr_parents):
        indice_max_fitness = np.where(fitness == np.max(fitness))
        parents[i,:] = population[indice_max_fitness[0][0], :]
        fitness[indice_max_fitness[0][0]] = -999999
    return parents

def croisement(parents, nbr_enfants):
    enfants = np.empty((nbr_enfants, parents.shape[1]))
    point_de_croisement = int(parents.shape[1]/2) #croisement au milieu
    taux_de_croisement = 0.8
    i=0
    while (i < nbr_enfants): #parents.shape[0]
        indice_parent1 = i%parents.shape[0]
        indice_parent2 = (i+1)%parents.shape[0]
        x = rd.random()
        if x > taux_de_croisement: # parents stériles
            continue
        indice_parent1 = i%parents.shape[0]
        indice_parent2 = (i+1)%parents.shape[0]
        enfants[i,0:point_de_croisement] = parents[indice_parent1,0:point_de_croisement]
        enfants[i,point_de_croisement:] = parents[indice_parent2,point_de_croisement:]
        i+=1
    return enfants

# La mutation consiste à inverser le bit
def mutation(enfants):
    mutants = np.empty((enfants.shape))
    taux_mutation = 0.5
    for i in range(mutants.shape[0]):
        random_valeur = rd.random()
        mutants[i,:] = enfants[i,:]
        if random_valeur > taux_mutation:
            continue
        int_random_valeur = randint(0,enfants.shape[1]-1) #choisir aléatoirement le bit à inverser   
        if mutants[i,int_random_valeur] == 0 :
            mutants[i,int_random_valeur] = 1
        else :
            mutants[i,int_random_valeur] = 0
    return mutants  

def optimize(poids, valeur, population, pop_size, nbr_generations, capacite):
    sol_opt, historique_fitness = [], []
    nbr_parents = pop_size[0]//2
    nbr_enfants = pop_size[0] - nbr_parents 
    for i in range(nbr_generations):
        fitness = cal_fitness(poids, valeur, population, capacite)
        historique_fitness.append(fitness)
        parents = selection(fitness, nbr_parents, population)
        enfants = croisement(parents, nbr_enfants)
        mutants = mutation(enfants)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants
    print('Voici la dernière génération de la population: \n{}\n'.format(population)) 
    fitness_derniere_generation = cal_fitness(poids, valeur, population, capacite)      
    print('Fitness de la dernière génération: \n{}\n'.format(fitness_derniere_generation))
    max_fitness = np.where(fitness_derniere_generation == np.max(fitness_derniere_generation))
    sol_opt.append(population[max_fitness[0][0],:])
    return sol_opt, historique_fitness

#paramètres de l'algorithme génétique
#lancement de l'algorithme génétique
sol_opt, historique_fitness = optimize(poids, valeur, population_initiale, pop_size, nbr_generations, capacite_max)


#affichage du résultat
print('La solution optimale est: \n{}'.format(sol_opt))
print(np.asarray(historique_fitness).shape)
print('Avec une valeur de : ',np.amax(historique_fitness),'€ et un poids de  : ', np.sum(sol_opt * poids),'kg')
print('Les objet qui maximisent la valeur contenue dans le sac sans le déchirer :')
objets_selectionnes = ID_objets * sol_opt
for i in range(objets_selectionnes.shape[1]):
  if objets_selectionnes[0][i] != 0:
     print(f'{objets_selectionnes[0][i]}')

     
historique_fitness_moyenne = [np.mean(fitness) for fitness in historique_fitness]
historique_fitness_max = [np.max(fitness) for fitness in historique_fitness]
plt.plot(list(range(nbr_generations)), historique_fitness_moyenne, label = 'Valeurs moyennes')
plt.plot(list(range(nbr_generations)), historique_fitness_max, label = 'Valeur maximale')
plt.legend()
plt.title('Evolution de la Fitness à travers les générations')
plt.xlabel('Génerations')
plt.ylabel('Fitness')
plt.show()