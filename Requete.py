from random import randint
from random import random
from math import exp

class Requete:

    def __init__(self, temps, categorie):
        self.temps = temps
        self.categorie = categorie

# Renvoie le temps d'arrivée de la prochaine requête et sa catégorie,
#  donnée respetivement selon la loi exponentielle et la loi uniforme
def nouvelleRequete(nbCategories, _lambda, temps):
    categorie = randint(1, nbCategories)
    x = random()
    t = 1/ (_lambda / exp(-_lambda * x))
    return Requete(t + temps, categorie)

def tester_nouvelle_requete(nbCat, _lambda):
    t = 0
    for _ in range(0, 50):
        r = nouvelleRequete(nbCat, _lambda, t)
        t = r.temps
        print("requete cat=" + str(r.categorie) + " t=" + str(r.temps))