from Server import Server

class ServerGroup:
    def __init__(self, identifiant_groupe, nombre_serveurs, taux_service):
        self.identifiant_groupe = identifiant_groupe
        self.serveurs = [Server(f"{identifiant_groupe}-{i}") for i in range(nombre_serveurs)]
        self.taux_service = taux_service

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
