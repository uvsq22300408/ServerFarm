import random

class Server:
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self.occupe = False
        self.fin_traitement = 0.0  # Instant où il sera libre
        self.tempsTravail = 0.0

    # Met à jour le temps que le serveur met pour traiter une requête
    def setTempsTavail(self, durée):
        self.tempsTravail = durée

    def assigner_requete(self, temps_actuel, taux_service):
        self.occupe = True
        duree_service = random.expovariate(taux_service)
        self.fin_traitement = temps_actuel + duree_service

        facteur_ref = (4 / 20) / taux_service  # Comparaison avec cas non spécialisé
        #print(f"Serveur {self.identifiant} assigne la requête.")
        #print(f"Temps de traitement généré : {duree_service:.4f} unités")
        #print(f"Traitement {facteur_ref:.2f}x plus rapide que sans spécialisation")

        return self.fin_traitement

    def mettre_a_jour(self, temps_actuel):
        if self.occupe and temps_actuel >= self.fin_traitement:
            self.occupe = False
