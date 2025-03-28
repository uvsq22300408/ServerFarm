import random

class Server:
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self.occupe = False
        self.fin_traitement = 0.0  # Instant où il sera libre

    def assigner_requete(self, temps_actuel, taux_service):
        self.occupe = True
        duree_service = random.expovariate(taux_service)
        self.fin_traitement = temps_actuel + duree_service
        return duree_service

    def mettre_a_jour(self, temps_actuel):
        if self.occupe and temps_actuel >= self.fin_traitement:
            self.occupe = False
