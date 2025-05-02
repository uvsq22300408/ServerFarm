from collections import deque
from ServerGroup import ServerGroup
from Event import Event
from eventType import EventType

class Routeur:

    NON_SPECIALISE = -1

    def __init__(self, capacite_file, nb_categories, c_param):
        self.file = deque()
        self.capacite_max = capacite_file
        self.nb_categories = nb_categories
        self.temps_traitement = (c_param - 1) / c_param
        self.requete_en_cours = None
        self.temps_disponible = 0.0
        self.requetes_perdues = 0
        self.requetes_traitees = 0
        self.requetes_recues = 0
        self.groupes = []
        self.specialites = []

    # Ajoute al requete a la file. Retourne True si la requete a pu etre ajoutee, False sinon
    #  (la file est pleine) 
    def ajouter_requete(self, requete, temps_actuel):
        self.requetes_recues += 1
        if len(self.file) < self.capacite_max:
            self.file.append(requete)
            requete.transmiseRouteur = True
            return True
        else:
            requete.marquer_comme_perdue()
            self.requetes_perdues += 1
            return False

    # Traite la requête et retourne la date de fin de traitement (date a laquelle le routeur sera de nouveau libre)
    def traiter(self, temps_actuel):
        if self.requete_en_cours is None and self.file:
            self.requete_en_cours = self.file.popleft()
            self.requete_en_cours.definir_debut_traitement(temps_actuel)
            self.temps_disponible = temps_actuel + self.temps_traitement
            self.requetes_traitees += 1
        return Event(EventType.RouteurDisponible, self.temps_disponible)

    # Envoie la requete au groupe approprie si possible
    def envoieRequete(self, tempsActuel):
        req = self.requete_en_cours
        # Sélectionne un groupe associé à la requête si disposible
        # Si pas de groupe spécialisé disponible, on cherche un groupe non-spécialisé
        groupe = self.chercheGroupe(req.categorie)
        if groupe == None:
            # Si aucun groupe disponible, la requête est mide en attente, le routeur est bloqué
            return self.routeurBloqué(tempsActuel)
        # Sélectionne un serveur libre du groupe et lui associe la requête
        serveur = groupe.chercheServeurLibre()
        if serveur == None:
            # Si aucun serveur disponible, la requête est mise en attente, le routeur est bloqué
            return self.routeurBloqué(tempsActuel)
        if groupe.spécialisé:
            fin_traitement = serveur.assigner_requete(tempsActuel, groupe.taux_serviceSpécialisé)
        else:
            fin_traitement = serveur.assigner_requete(tempsActuel, groupe.taux_service)
        req.temps_fin_traitement = fin_traitement
        # Le routeur n'est plus en train de traiter une requête
        self.requete_en_cours = None
        return self.routeurEnvoieSuccès(tempsActuel)

    def taux_perte(self):
        total = self.requetes_traitees + self.requetes_perdues
        return self.requetes_perdues / total if total > 0 else 0.0


    def chercheGroupe(self, catégorie):
        # Renvoie le premier groupe spécialisé correspondant à catégorie
        # qui possède un serveur non-occupé
        # Si aucun disponible, renvoie un groupe non spécialisé
        groupeNonSpé = None
        for groupeIndex in range(0, len(self.groupes)):
            if self.specialites[groupeIndex] == catégorie:
                g = self.groupes[groupeIndex]
                if g.serveur_disponible():
                    return g
            elif self.specialites[groupeIndex] == Routeur.NON_SPECIALISE and groupeNonSpé == None:
                groupeNonSpé = self.groupes[groupeIndex]
                if not groupeNonSpé.serveur_disponible():
                    groupeNonSpé = None
        return groupeNonSpé
    
    # Renvoie un événement routeurBloqué avec la date de fin de traitement 
    # d'une requête par un sevreur la plus proche chronologiquement
    def routeurBloqué(self, tempsActuel):
        # Trouve le seveur finissant son traitement le plus tôt et renvoie la date à laquelle
        # il sera libre
        mini = None
        for g in self.groupes:
            for s in g.serveurs:
                if s.occupe and (mini == None or s.fin_traitement < mini):
                    mini = s.fin_traitement
        if mini == None:
            print("Le routeur est bloqué mais aucun serveur n'est occupé. La catégorie de la requête n'est donc pas acceptable par le routeur.")
            exit()
        return Event(eventType=EventType.RouteurBloqué, temps=tempsActuel, fin=mini)
    
    # Renvoie un événement routeurEnvoieSuccès
    def routeurEnvoieSuccès(self, tempsActuel):
        return Event(eventType=EventType.RouteurEnvoieSucces, temps=tempsActuel)