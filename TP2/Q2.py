# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Ã‰diteur de Spyder

Ceci est un script temporaire.
"""

# RÃ©solution du problÃ¨me du voyageur de commerce ou TCS Ã  l'aide du recuit simulÃ©
# import de la librairie
import random
import numpy as np



# DonnÃ©es du problÃ¨me (gÃ©nÃ©rÃ©es alÃ©atoirement)
NOMBRE_DE_VILLES = 10
distances = np.zeros((NOMBRE_DE_VILLES, NOMBRE_DE_VILLES))
for ville in range(NOMBRE_DE_VILLES):
    villes = [ i for i in range(NOMBRE_DE_VILLES) if not i == ville ]
    for vers_la_ville in villes:
        distances[ville][vers_la_ville] =random.randint(50, 2000)
        distances[vers_la_ville][ville] =distances[vers_la_ville][ville]

print('voici la matrice des distances entres les villes \n',distances)



def cal_distance(solution,distances,NOMBRE_DE_VILLES):
    eval_distance=0
    for i in range (len(solution)):
        origine,destination=solution[i],solution[(i+1)%NOMBRE_DE_VILLES]
        eval_distance+=distances[origine][destination]
    return eval_distance


def voisinage(solution):
    echange=random.sample(range(NOMBRE_DE_VILLES),2)
    sol_voisine=solution
    (sol_voisine[echange[0]],sol_voisine[echange[1]])=(sol_voisine[echange[1]],sol_voisine[echange[0]])
    return sol_voisine
 
    
# recuit simulÃ©
solution=random.sample(range(NOMBRE_DE_VILLES),NOMBRE_DE_VILLES)
cout0=cal_distance(solution,distances,NOMBRE_DE_VILLES)
T=30
facteur=0.99
T_intiale=T
for i in range(100):
    print('la ',i,'Ã¨me solution = ',solution,' distance totale= ',cout0,' tempÃ©rature actuelle =',T)
    T=T*facteur
    for j in range(50):
        nouv_sol=voisinage(solution)
        cout1=cal_distance(nouv_sol,distances,NOMBRE_DE_VILLES)
        if cout1<cout0:
            cout0=cout1
            solution=nouv_sol
        else:
            x=np.random.uniform()
            if x<np.exp((cout0-cout1)/T):
                cout0=cout1
                solution=nouv_sol
