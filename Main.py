from ServerGroup import ServerGroup
from Routeur import Routeur
from Requete import Requete, tester_nouvelle_requete, nouvelleRequete
from Event import Event
from eventType import EventType


def main():
    # Parametres
    ## TODO : Prendre depuis les arguments du programme OU depuis un fichier
    c = 1
    nbCategories = 6
    _lambda = 1
    limiteTemps = 1000
    # Environnement
    nbServeurs = 12
    temps = 0
    routeur = Routeur()
    echeancier = []
    requetes = []
    groupes = []
    # TODO : Créer les groupes de serveurs
    for groupeId in range(0, c):
        taux_service = calculTauxService(c)
        g = ServerGroup(groupeId, nbServeurs / c, taux_service)
        groupes.append(g)
    # TODO : Spécialiser les groupes de serveurs selon les choix de l'utilisateur
    # Ajouter une première requête
    req = nouvelleRequete(nbCategories, _lambda, temps)
    echeancier.append(Event(EventType.Arrive, req.temps))
    requetes.append(req)

    # Boucle de traitement des événements
    while (simulationNonTerminee(temps)):
        event: Event = echeancier.pop(0)
        # On met à jour la date de la simulation
        temps = event.temps
        # TODO: On met à jour les groupes de serveurs

        match (event.eventType):
            case EventType.Arrive:
                # Gère l'arrivée d'une nouvelle requête
                ## TODO: On ajoute la catégorie de la requête au routeur
                req = requetes.pop(0)

                # Prépare l'envoi de la prochaine requête
                req = nouvelleRequete(nbCategories, _lambda, temps)
                echeancier.append(Event(EventType.Arrive, req.temps))
                break
            case default:
                break




# Renvoie true si le temps de simulation a dépassé la limite, false sinon
def simulationNonTerminee(temps, limiteTemps):
    return temps < limiteTemps

# Renvoie le taux de service selon le nombre de groupe
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
        case default:
            raise Exception("C n'a pas une valeur valide. Sa valeur doit être 1, 2, 3 ou 6. Sa valeur actuelle est " + c)
    

def tester_groupe_serveurs():
    temps_actuel = 0.0
    taux_service = 4 / 20  # Exemple : pour C = 1
    groupe = ServerGroup(identifiant_groupe="A", nombre_serveurs=3, taux_service=taux_service)

    print("=== Début de la simulation de test ===")
    
    # Simulation de 5 requêtes arrivant toutes les 2 unités de temps
    for i in range(5):
        print(f"\nRequête {i+1} arrivée au temps {temps_actuel:.1f}")
        
        # Met à jour l'état des serveurs avant d’assigner une nouvelle requête
        groupe.mettre_a_jour_serveurs(temps_actuel)

        if groupe.serveur_disponible():
            duree = groupe.assigner_a_serveur_disponible(temps_actuel)
            print(f"Reqete assignée. Duree de traitment : {duree:.2f}")
        else:
            print("Requête non assignée.")

        # On avance le temps pour simuler l'arrivée progressive des requêtes
        temps_actuel += 2.0

    print("\n=== Fin du test ===")

if __name__ == "__main__":
    tester_nouvelle_requete(6, 1)
    tester_groupe_serveurs()
