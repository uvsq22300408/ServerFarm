from collections import deque
from Requete import Requete
from ServerGroup import GroupeServeurs

class Routeur:
    def __init__(self, capacite_file, nb_categories, c_param):
        self.file = deque()
        self.capacite_max = capacite_file
        self.nb_categories = nb_categories
        self.temps_traitement = (c_param - 1) / c_param
        self.requete_en_cours = None
        self.temps_disponible = 0.0  # Quand le routeur est libre
        self.requetes_perdues = 0
        self.requetes_traitees = 0

    def ajouter_requete(self, requete, temps_actuel):
        if len(self.file) < self.capacite_max:
            self.file.append(requete)
            return True
        else:
            requete.marquer_comme_perdue()
            self.requetes_perdues += 1
            return False

    def traiter(self, temps_actuel, groupes_serveurs):
        # Si le routeur est libre et qu'il y a des requêtes en file
        if self.requete_en_cours is None and self.file:
            self.requete_en_cours = self.file.popleft()
            self.requete_en_cours.definir_debut_traitement(temps_actuel)
            self.temps_disponible = temps_actuel + self.temps_traitement

        # Si le traitement de la requête en cours est terminé
        if self.requete_en_cours and temps_actuel >= self.temps_disponible:
            categorie = self.requete_en_cours.categorie
            groupe = groupes_serveurs[categorie - 1]  # Catégories commençant à 1
            groupe.mettre_a_jour_serveurs(temps_actuel)

            if groupe.serveur_disponible():
                duree_service = groupe.assigner_a_serveur_disponible(temps_actuel)
                self.requete_en_cours.definir_fin_traitement(temps_actuel + duree_service)
                self.requetes_traitees += 1
                self.requete_en_cours = None
            # Sinon : on attend qu’un serveur du bon groupe se libère → on bloque

    def taux_perte(self):
        total = self.requetes_traitees + self.requetes_perdues
        if total == 0:
            return 0.0
        return self.requetes_perdues / total
