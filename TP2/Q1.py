import random
import numpy as np
import matplotlib.pyplot as plt
import time

def cal_distance_recuit(solution, distances, NOMBRE_DE_VILLES):
    eval_distance = 0
    for i in range(len(solution)):
        origine, destination = solution[i], solution[(i+1) % NOMBRE_DE_VILLES]
        eval_distance += distances[origine][destination]
    return eval_distance


def voisinage(solution, NOMBRE_DE_VILLES):
    echange = random.sample(range(NOMBRE_DE_VILLES), 2)
    sol_voisine = solution
    (sol_voisine[echange[0]], sol_voisine[echange[1]]) = (
        sol_voisine[echange[1]], sol_voisine[echange[0]])
    return sol_voisine

# Données
start_time = time.time()
NOMBRE_DE_VILLES = 10
distances = np.zeros((NOMBRE_DE_VILLES, NOMBRE_DE_VILLES))
MAX_DISTANCE = 2000
for ville in range(NOMBRE_DE_VILLES):
    villes = [i for i in range(NOMBRE_DE_VILLES) if not i == ville]
    for vers_la_ville in villes:
        distances[ville][vers_la_ville] = random.randint(50, MAX_DISTANCE)
        distances[vers_la_ville][ville] = distances[ville][vers_la_ville]
print('Matrice des distances entres les villes \n', distances)
print()

# Recuit
solution = random.sample(range(NOMBRE_DE_VILLES), NOMBRE_DE_VILLES)
cout0 = cal_distance_recuit(solution, distances, NOMBRE_DE_VILLES)
historique_distance=[]
T = 1000
facteur = 0.99
T_intiale = MAX_DISTANCE/2
min_sol = solution
temps = []
cout_min_sol = cout0
nbr_solutions = 1000
for i in range(nbr_solutions):
    historique_distance.append(cout0)
    T = T*facteur
    temps.append(T)
    for j in range(50):
        nouv_sol = voisinage(solution*1, NOMBRE_DE_VILLES)
        cout1 = cal_distance_recuit(nouv_sol, distances, NOMBRE_DE_VILLES)
        if cout1 < cout0:
            cout0 = cout1
            solution = nouv_sol
            if cout1 < cout_min_sol:
                cout_min_sol = cout1
                min_sol = solution
        else:
            x = np.random.uniform()
            if x < np.exp((cout0-cout1)/T):
                cout0 = cout1
                solution = nouv_sol

print('Voici la solution retenue ', min_sol, ' et son coût ',
      cal_distance_recuit(min_sol, distances, NOMBRE_DE_VILLES))

print("--- Temps d'éxécution : %ss ---" % (time.time() - start_time))

plt.plot(list(range(nbr_solutions)), historique_distance)
plt.plot(list(range(nbr_solutions)), temps)
plt.title('Evolution de la température en fonction des solutions')
plt.xlabel('i-ème solutions')
plt.ylabel('Température')
plt.show()
