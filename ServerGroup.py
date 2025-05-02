from Server import Server

class ServerGroup:
    def __init__(self, identifiant_groupe, nombre_serveurs, taux_service, spécialisé=False, 
                    taux_serviceSpécialisé=0):
        self.identifiant_groupe = identifiant_groupe
        self.serveurs = [Server(f"{identifiant_groupe}-{i}") for i in range(nombre_serveurs)]
        self.taux_service = taux_service
        self.taux_serviceSpécialisé = taux_serviceSpécialisé
        self.spécialisé = spécialisé

    def serveur_disponible(self):
        return any(not serveur.occupe for serveur in self.serveurs)

    def assigner_a_serveur_disponible(self, temps_actuel):
        for serveur in self.serveurs:
            if not serveur.occupe:
                return serveur.assigner_requete(temps_actuel, self.taux_service)
        return None  # Aucun serveur libre

    def mettre_a_jour_serveurs(self, temps_actuel):
        for serveur in self.serveurs:
            serveur.mettre_a_jour(temps_actuel)

    def chercheServeurLibre(self):
        for serveur in self.serveurs:
            if not serveur.occupe:
                return serveur
        return None
    
    # Met à jour le temps requis par les serveurs du groupe pour accomplir une tâche
    def setTempsTravail(self):
        if self.spécialisé:
            for s in self.serveurs:
                s.setTempsTavail(self.taux_serviceSpécialisé)
        else:
            for s in self.serveurs:
                s.setTempsTavail(self.taux_service)