from random import randint, random
from math import exp

class Requete:
    def __init__(self, temps_arrivee, categorie):
        self.temps = temps_arrivee
        self.categorie = categorie
        self.temps_debut_traitement = None
        self.temps_fin_traitement = None
        self.perdue = False

    def definir_debut_traitement(self, temps):
        self.temps_debut_traitement = temps

    def definir_fin_traitement(self, temps):
        self.temps_fin_traitement = temps

    def marquer_comme_perdue(self):
        self.perdue = True

    def est_terminee(self):
        return self.temps_fin_traitement is not None

    def temps_reponse(self):
        if self.temps_fin_traitement is None:
            return None
        return self.temps_fin_traitement - self.temps

def nouvelle_requete(nb_categories, _lambda, temps_actuel):
    categorie = randint(1, nb_categories)
    x = random()
    inter_arrivee = 1 / (_lambda / exp(-_lambda * x))
    temps_arrivee = temps_actuel + inter_arrivee
    return Requete(temps_arrivee, categorie)

def tester_nouvelle_requete(nb_categories, _lambda):
    t = 0
    for i in range(50):
        requete = nouvelle_requete(nb_categories, _lambda, t)
        t = requete.temps
        print(f"Requête {i+1:02d} | Catégorie : {requete.categorie} | Temps d'arrivée : {requete.temps:.4f}")
