from ServerGroup import ServerGroup
from Routeur import Routeur
from Requete import Requete, tester_nouvelle_requete, nouvelle_requete
from Event import Event
from eventType import EventType


def main():
    # Paramètres
    c = 1  # Nombre de groupes de serveurs
    nbCategories = c  # Une catégorie par groupe
    _lambda = 1
    limiteTemps = 1000

    # Environnement
    nbServeurs = 12
    temps = 0
    routeur = Routeur(capacite_file=100, nb_categories=nbCategories, c_param=c)
    echeancier = []
    requetes = []
    groupes = []

    # Création des groupes de serveurs
    for groupeId in range(c):
        taux_service = calculTauxService(c)
        g = ServerGroup(groupeId, int(nbServeurs / c), taux_service)
        groupes.append(g)

    # Ajout d'une première requête
    req = nouvelle_requete(nbCategories, _lambda, temps)
    echeancier.append(Event(EventType.Arrive, req.temps))
    requetes.append(req)

    # Boucle de simulation
    while simulationNonTerminee(temps, limiteTemps):
        event = echeancier.pop(0)
        temps = event.temps

        # Mettre à jour les serveurs à chaque événement
        for g in groupes:
            g.mettre_a_jour_serveurs(temps)

        match event.eventType:
            case EventType.Arrive:
                # Récupère et traite la requête en attente
                req = requetes.pop(0)
                routeur.ajouter_requete(req, temps)
                routeur.traiter(temps, groupes)

                # Génère une nouvelle requête
                req = nouvelle_requete(nbCategories, _lambda, temps)
                echeancier.append(Event(EventType.Arrive, req.temps))
                requetes.append(req)
            case _:
                pass


def simulationNonTerminee(temps, limiteTemps):
    return temps < limiteTemps


def calculTauxService(c):
    match c:
        case 1:
            return 4 / 20
        case 2:
            return 7 / 20
        case 3:
            return 10 / 20
        case 6:
            return 14 / 20
        case _:
            raise Exception(f"C invalide ({c}). Doit être 1, 2, 3 ou 6.")


if __name__ == "__main__":
    main()
