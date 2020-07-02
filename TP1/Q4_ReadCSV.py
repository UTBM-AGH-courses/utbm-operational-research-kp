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
import csv

# Données du problème (générées aléatoirement)
nombre_actions = 35     # Nombre d'actions
budget = 5000           # Budget 
nbr_generations = 100   # Nombre de générations

ID_actions = []                # ID des actions à mettre dans le sac
prix = [] 
benef_attendu = []  # Gains des actions attendus

with open('data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        ID_actions = np.append(ID_actions, int(row[0]))
        prix = np.append(prix,int(row[1]))
        benef_attendu = np.append(benef_attendu, float(row[2]))
    print(ID_actions)

print('La liste des objet est la suivante :')
print('ID_actions      Prix      Benéfice par mois attendu')


for i in range(ID_actions.shape[0]):
    print(f'{ID_actions[i]} \t\t {prix[i]} \t\t {benef_attendu[i]}')
print()


def check_risk(row, prix, budget):
    for i in range(len(row)):
        if (row[i] > 1 and (row[i]*prix[i])>budget*0.25):
            return False

def generer_tableau(population, prix, budget):
    tableau = []
    for i in range(population[0]):
        row = np.random.binomial(5, 0.3 , size = pop_size[1])
        mult = np.multiply(row,prix)
        check_risk(row, prix, budget)
        while(np.sum(mult) > budget or check_risk(row, prix, budget) == False):
            row = np.random.binomial(5, 0.3 , size = pop_size[1])
            mult = np.multiply(row,prix)
        print('ligne ', i, ' OK')
        print(np.sum(mult))
        tableau.append(row.tolist())
    return np.array(tableau, dtype=np.int)


# Créer la population initiale
population = 8 # La taille de la population 
pop_size = (population, ID_actions.shape[0])
#population_initiale = np.random.randint(2, size = pop_size)
population_initiale = generer_tableau(pop_size, prix, budget)
population_initiale = population_initiale.astype(int)

print('Taille de la population = {}'.format(pop_size))
print('Population Initiale: \n{}'.format(population_initiale))

    

def cal_fitness(prix, benef_attendu, population, budget):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * benef_attendu)
        S2 = np.sum(population[i] * prix)
        if S2 <= budget:
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

def optimize(prix, benef_attendu, population, pop_size, nbr_generations, budget):
    sol_opt, historique_fitness = [], []
    nbr_parents = pop_size[0]//2
    nbr_enfants = pop_size[0] - nbr_parents 
    for i in range(nbr_generations):
        fitness = cal_fitness(prix, benef_attendu, population, budget)
        historique_fitness.append(fitness)
        parents = selection(fitness, nbr_parents, population)
        enfants = croisement(parents, nbr_enfants)
        mutants = mutation(enfants)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants
    print('Voici la dernière génération de la population: \n{}\n'.format(population)) 
    fitness_derniere_generation = cal_fitness(prix, benef_attendu, population, budget)      
    print('Fitness de la dernière génération: \n{}\n'.format(fitness_derniere_generation))
    max_fitness = np.where(fitness_derniere_generation == np.max(fitness_derniere_generation))
    sol_opt.append(population[max_fitness[0][0],:])
    return sol_opt, historique_fitness

#paramètres de l'algorithme génétique
#lancement de l'algorithme génétique
sol_opt, historique_fitness = optimize(prix, benef_attendu, population_initiale, pop_size, nbr_generations, budget)


#affichage du résultat

print('La solution optimale est: \n{}'.format(sol_opt))
print(np.asarray(historique_fitness).shape)
print('Avec un portefeuille d\'actions d\'une valeur totale en-devenir de : ',np.amax(historique_fitness),'€ par mois, et pour un total dépensé de : ', np.sum(sol_opt * prix),'€')
print('Les objet qui maximisent la valeur du portefeuille sans dépasser le budget :')
objets_selectionnes = ID_actions * sol_opt
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