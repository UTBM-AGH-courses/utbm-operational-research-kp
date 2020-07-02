# TP AD70

Valentin REVERSAT 🏍
Thomas MARTIN

# Q1
 Si le nombre d'objets est trop grand par rapport à la capacité du sac (le sac craque), on ne peut pas trouver une solution optimal car la fitness sera a zéro.

 La modification de la valeur max de la valeur d'un objet ou encore de taille du sac a pour effet de modifier la valeur de départ de la fitness.


# Q2
 Afin de ne traiter que les solutions possibles, il faut éviter un cas où le nombre d'objet serait trop important avec une capacité du sac trop faible, puisque la fitness serait alors nulle et il n'y aurait pas de solution.

 Au lieu de générer la tableau de départ aléatoirement, nous avons donc ajouté une fonction générer ce tableau (`lignes = nombre de candidats` et `colonnes = 1 si objet récupéré | 0 sinon`).

 ```PYTHON
    def generer_tableau(population, poids, capacite_max):
    tableau = []
    for i in range(population[0]):
        row = np.random.randint(2, size = pop_size[1])
        mult = np.multiply(row,poids)
        while(np.sum(mult) > capacite_max):
            row = np.random.randint(2, size = pop_size[1])
            mult = np.multiply(row,poids)
        tableau.append(row.tolist())
    return np.array(tableau, dtype=np.int)


    population_initiale = generer_tableau(pop_size, poids, capacite_max)
 ```


# Q3
Nous avons ajouté une fonction `check_risk` et nous avons modifié `generer_tableau` afin de permettre d'insérer des entitiés et non plus seulement 0 ou 1 à l'aide d'une loi binomiale


 ```PYTHON
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
            while(np.sum(mult) > budget and check_risk(row, prix, budget) == False):
                row = np.random.binomial(5, 0.3 , size = pop_size[1])
                mult = np.multiply(row,prix)
            tableau.append(row.tolist())
        return np.array(tableau, dtype=np.int)
 ```


 # Q4
 Nous avons généré les fichiers de données (data[2-4].csv) mais nous ne sommes pas parvenu a trouver une configuration permettant d'améliorer la rapidité d'éxécution du code
 

