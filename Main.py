from ServerGroup import ServerGroup
from Routeur import Routeur
from Requete import Requete, tester_nouvelle_requete, nouvelle_requete
from Event import Event
from eventType import EventType


def main():
    # Paramètres
    c = 2  # Nombre de groupes de serveurs
    nbCategories = c  # Une catégorie par groupe
    _lambda = 0.2
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
    while simulationNonTerminee(temps, limiteTemps) and calculTauxPerte(sauvegarde_requetes) < 5:
        event = echeancier.pop(0)
        temps = event.temps
        print("temps = " + str(temps))
        # Si le routeur doit être libéré avant le prochain événement on le libère.
        # Le routeur libéré doit maintenant envoyer la requête à un sevreur viable.
        # Si l'envoie échoue, le serveur reste bloqué
        if (not routeurLibre) and routeurDateLiberation < temps:
            print("routeur libéré")
            routeurLibre = True
            routeurDisponibleEvent = None
            routeurDateLiberation = 0.0
            envoieRequeteEvent = routeur.envoieRequete(routeurDateLiberation)
            if envoieRequeteEvent.eventType == EventType.RouteurBloqué:
                print("Routeur Bloqué jusqu'à " + str(envoieRequeteEvent.fin))
                routeurLibre = False
                routeurDateLiberation = envoieRequeteEvent.fin
        
        # Mettre à jour les serveurs à chaque événement
        for g in groupes:
            g.mettre_a_jour_serveurs(temps)

        match event.eventType:
            case EventType.Arrive:
                print("arrivée requete: " + str(req.temps))
                # Récupère et traite la requête en attente
                req = requetes.pop(0)
                isRequeteAjoutee = routeur.ajouter_requete(req, temps)
                # Si la requete a ete ajoutee on essaie de la traiter. Sinon elle est perdue
                if isRequeteAjoutee:
                    if routeurLibre:
                        routeurDisponibleEvent = routeur.traiter(temps)
                        routeurLibre = False
                        routeurDateLiberation = routeurDisponibleEvent.temps
                else:
                    req.perdue = True
                # Génère une nouvelle requête
                req = nouvelle_requete(nbCategories, _lambda, temps)
                echeancier.append(Event(EventType.Arrive, req.temps))
                requetes.append(req)
                sauvegarde_requetes.append(req)
            case _:
                pass
    print("routeur taux de perte: " + str(calculTauxPerte(sauvegarde_requetes)) + "%")
    print("routeur temps moyen de traitement: " + str(calculTempsMoyenTraitement(sauvegarde_requetes)))
    print("routeur pourcentage de requêtes vues = " + str((routeur.requetes_recues / len(sauvegarde_requetes)) * 100) + "%")
    print("routeur pourcentage de requêtes traitées parmi les requêtes reçues = " + str((routeur.requetes_traitees / routeur.requetes_recues) * 100) + "%")
    print("     nb requêtes reçues par le routeur: " + str(routeur.requetes_recues))
    print("     nb requêtes traitées par le routeur: " + str(routeur.requetes_traitees))
    print("     nb requêtes perdues: " + str(routeur.requetes_perdues))
    #logRequetes(sauvegarde_requetes)


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
    nbTraitées = 0
    for r in sauvegarde_requetes:
        if r.perdue == False and r.temps_fin_traitement != None:
            if r.temps_fin_traitement > r.temps:
                total += r.temps_fin_traitement - r.temps
                nbTraitées += 1
    if nbTraitées == 0:
        print("0 requêtes traitées")
        return 0
    return total / nbTraitées

def calculTauxPerte(sauvegarde_requetes):
    total = 0
    for r in sauvegarde_requetes:
        if r.perdue:
            total += 1
    print("     total = " + str(total))
    print("     len(sauvegarde_requetes) = " + str(len(sauvegarde_requetes)))
    return (total / len(sauvegarde_requetes)) * 100

def logRequetes(sauvegarde_requetes):
    for r in sauvegarde_requetes:
        print(r.toString())

if __name__ == "__main__":
    #tester_nouvelle_requete(6, 1)
    main()