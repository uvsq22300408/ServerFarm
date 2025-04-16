from collections import deque
from ServerGroup import ServerGroup

class Routeur:
    def __init__(self, capacite_file, nb_categories, c_param):
        self.file = deque()
        self.capacite_max = capacite_file
        self.nb_categories = nb_categories
        self.temps_traitement = (c_param - 1) / c_param
        self.requete_en_cours = None
        self.temps_disponible = 0.0
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
        if self.requete_en_cours is None and self.file:
            self.requete_en_cours = self.file.popleft()
            self.requete_en_cours.definir_debut_traitement(temps_actuel)
            self.temps_disponible = temps_actuel + self.temps_traitement

        if self.requete_en_cours and temps_actuel >= self.temps_disponible:
            categorie = self.requete_en_cours.categorie
            groupe = groupes_serveurs[categorie - 1]  # Catégorie entre 1 et nb
            groupe.mettre_a_jour_serveurs(temps_actuel)

            if groupe.serveur_disponible():
                duree_service = groupe.assigner_a_serveur_disponible(temps_actuel)
                self.requete_en_cours.definir_fin_traitement(temps_actuel + duree_service)
                self.requetes_traitees += 1
                self.requete_en_cours = None

    def taux_perte(self):
        total = self.requetes_traitees + self.requetes_perdues
        return self.requetes_perdues / total if total > 0 else 0.0
