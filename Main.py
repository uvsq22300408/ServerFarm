from ServerGroup import ServerGroup
from Routeur import Routeur
from Requete import Requete, tester_nouvelle_requete, nouvelle_requete
from Event import Event
from eventType import EventType


def main():
    # Paramètres
    c = 6  # Nombre de groupes de serveurs
    nbCategories = c  # Une catégorie par groupe
    _lambda = 1
    limiteTemps = 1000
    facteurAccélérationSpécialisé = 1.5

    # Environnement
    nbServeurs = 12
    temps = 0
    routeur = Routeur(capacite_file=100, nb_categories=nbCategories, c_param=c)
    echeancier = []
    requetes = []
    sauvegarde_requetes = []
    groupes = []
    spécialités = [1, 2, 3, 4, 5, 6, 1]
    routeurLibre = True
    routeurDateLiberation = 0.0
    routeurDisponibleEvent = None

    # Création des groupes de serveurs
    for groupeId in range(c):
        taux_service = calculTauxService(c)
        if spécialités[groupeId] != Routeur.NON_SPECIALISE:
            g = ServerGroup(groupeId, int(nbServeurs / c), taux_service, spécialisé=True,
                            taux_serviceSpécialisé=taux_service / facteurAccélérationSpécialisé)
        else:
            g = ServerGroup(groupeId, int(nbServeurs / c), taux_service)
        
        groupes.append(g)
    routeur.groupes = groupes
    routeur.specialites = spécialités
    
    # Ajout d'une première requête
    req = nouvelle_requete(nbCategories, _lambda, temps)
    echeancier.append(Event(EventType.Arrive, req.temps))
    requetes.append(req)
    sauvegarde_requetes.append(req)

    # Boucle de simulation. On s'arrete a limiteTemps ou lorsqu'on atteint 5% de pertes. 
    while simulationNonTerminee(temps, limiteTemps) and calculTauxPerte(sauvegarde_requetes) < (1/20):
        event = echeancier.pop(0)
        temps = event.temps
        # Si le routeur doit être libéré avant le prochain événement on le libère,
        # on remet ensuite l'autre evenement dans la file pour le traiter a l'iteration suivante.
        # Le routeur libéré doit maintenant envoyer la requête à un sevreur viable.
        # Si l'envoie échoue, le serveur reste bloqué
        if (not routeurLibre) and routeurDateLiberation < temps:
            routeurLibre = True
            routeurDisponibleEvent = None
            routeurDateLiberation = 0.0
            routeur.envoieRequete(routeurDateLiberation)
            echeancier.insert(0, event)
        
        # Mettre à jour les serveurs à chaque événement
        for g in groupes:
            g.mettre_a_jour_serveurs(temps)

        match event.eventType:
            case EventType.Arrive:
                # Récupère et traite la requête en attente
                req = requetes.pop(0)
                isRequeteAjoutee = routeur.ajouter_requete(req, temps)
                # Si la requete a ete ajoutee on essaie de la traiter. Sinon elle est perdue
                if isRequeteAjoutee:
                    if routeurLibre:
                        routeurDisponibleEvent = routeur.traiter(temps)
                        routeurLibre = False
                        routeurDateLiberation = routeurDisponibleEvent.temps

                # Génère une nouvelle requête
                req = nouvelle_requete(nbCategories, _lambda, temps)
                echeancier.append(Event(EventType.Arrive, req.temps))
                requetes.append(req)
                sauvegarde_requetes.append(req)
            case _:
                pass
    print("routeur taux de perte: " + str(calculTauxPerte(sauvegarde_requetes)))
    print("routeur temps moyen de traitement: " + str(calculTempsMoyenTraitement(sauvegarde_requetes)))


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

def calculTempsMoyenTraitement(sauvegarde_requetes):
    total = 0
    for r in sauvegarde_requetes:
        if r.perdue == False and r.temps_fin_traitement != None:
            if r.temps_fin_traitement > r.temps:
                total += r.temps_fin_traitement - r.temps
    print("     total = " + str(total))
    print("     len(sauvegarde_requetes) = " + str(len(sauvegarde_requetes)))
    return total / len(sauvegarde_requetes)

def calculTauxPerte(sauvegarde_requetes):
    total = 0
    for r in sauvegarde_requetes:
        if r.perdue:
            total += 1
    print("     total = " + str(total))
    print("     len(sauvegarde_requetes) = " + str(len(sauvegarde_requetes)))
    return total / len(sauvegarde_requetes)

if __name__ == "__main__":
    main()