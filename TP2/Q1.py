# Résolution du problème du voyageur de commerce ou TCS à l'aide du recuit simulé
# Import des librairies
import random
import numpy as np
import matplotlib.pyplot as plt


# Données du problème (génération aléatoire)
NOMBRE_DE_VILLES = 10
distances = np.zeros((NOMBRE_DE_VILLES, NOMBRE_DE_VILLES))
for ville in range(NOMBRE_DE_VILLES):
    villes = [i for i in range(NOMBRE_DE_VILLES) if not i == ville]
    for vers_la_ville in villes:
        distances[ville][vers_la_ville] = random.randint(50, 2000)
        distances[vers_la_ville][ville] = distances[vers_la_ville][ville]

print('Voici la matrice des distances entres les villes \n', distances)


def cal_distance(solution, distances, NOMBRE_DE_VILLES):
    eval_distance = 0
    for i in range(len(solution)):
        origine, destination = solution[i], solution[(i+1) % NOMBRE_DE_VILLES]
        eval_distance += distances[origine][destination]
    return eval_distance


def voisinage(solution):
    echange = random.sample(range(NOMBRE_DE_VILLES), 2)
    sol_voisine = solution
    (sol_voisine[echange[0]], sol_voisine[echange[1]]) = (
        sol_voisine[echange[1]], sol_voisine[echange[0]])
    return sol_voisine


# recuit simulÃ©
solution = random.sample(range(NOMBRE_DE_VILLES), NOMBRE_DE_VILLES)
cout0 = cal_distance(solution, distances, NOMBRE_DE_VILLES)
T = 30
facteur = 0.99
nbr_solutions = 300
temps = []
T_intiale = T
for i in range(nbr_solutions):
    print('La ', i, 'ème solution = ', solution,
          ' distance totale= ', cout0, ' température actuelle =', T)
    temps.append(T)
    T = T*facteur
    for j in range(50):
        nouv_sol = voisinage(solution)
        cout1 = cal_distance(nouv_sol, distances, NOMBRE_DE_VILLES)
        if cout1 < cout0:
            cout0 = cout1
            solution = nouv_sol
        else:
            x = np.random.uniform()
            if x < np.exp((cout0-cout1)/T):
                cout0 = cout1
                solution = nouv_sol


plt.plot(list(range(nbr_solutions)), temps)
plt.title('Evolution de la température en fonction des solutions')
plt.xlabel('i-ème solutions')
plt.ylabel('Température')
plt.show()
