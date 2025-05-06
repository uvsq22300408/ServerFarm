from ServerGroup import ServerGroup
from Routeur import Routeur
from Requete import Requete, tester_nouvelle_requete, nouvelle_requete
from Event import Event
from eventType import EventType
import io

import seaborn as sns
import pandas
import matplotlib.pyplot as plt

def main(c, _lambda):
    # Paramètres
    # Nombre de groupes de serveurs
    nbCategories = c  # Une catégorie par groupe
    limiteTemps = 1000

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
                            taux_serviceSpécialisé=taux_service)
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
        #print("temps = " + str(temps))
        # Si le routeur doit être libéré avant le prochain événement on le libère.
        # Le routeur libéré doit maintenant envoyer la requête à un sevreur viable.
        # Si l'envoie échoue, le serveur reste bloqué
        if (not routeurLibre) and routeurDateLiberation < temps:
            #print("routeur libéré")
            routeurLibre = True
            routeurDisponibleEvent = None
            routeurDateLiberation = 0.0
            envoieRequeteEvent = routeur.envoieRequete(routeurDateLiberation)
            if envoieRequeteEvent.eventType == EventType.RouteurBloqué:
                #print("Routeur Bloqué jusqu'à " + str(envoieRequeteEvent.fin))
                routeurLibre = False
                routeurDateLiberation = envoieRequeteEvent.fin
        
        # Mettre à jour les serveurs à chaque événement
        for g in groupes:
            g.mettre_a_jour_serveurs(temps)

        match event.eventType:
            case EventType.Arrive:
                #print("arrivée requete: " + str(req.temps))
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
    tauxPerte = calculTauxPerte(sauvegarde_requetes)
    tempsMoyen = calculTempsMoyenTraitement(sauvegarde_requetes)
    #print("routeur taux de perte: " + str(tauxPerte) + "%")
    #print("routeur temps moyen de traitement: " + str(tempsMoyen))
    #print("routeur pourcentage de requêtes vues = " + str((routeur.requetes_recues / len(sauvegarde_requetes)) * 100) + "%")
    #print("routeur pourcentage de requêtes traitées parmi les requêtes reçues = " + str((routeur.requetes_traitees / routeur.requetes_recues) * 100) + "%")
    #print("     nb requêtes reçues par le routeur: " + str(routeur.requetes_recues))
    #print("     nb requêtes traitées par le routeur: " + str(routeur.requetes_traitees))
    #print("     nb requêtes perdues: " + str(routeur.requetes_perdues))
    #logRequetes(sauvegarde_requetes)
    return (tauxPerte, tempsMoyen, routeur.requetes_traitees)

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
        #print("0 requêtes traitées")
        return 0
    return total / nbTraitées

def calculTauxPerte(sauvegarde_requetes):
    total = 0
    for r in sauvegarde_requetes:
        if r.perdue:
            total += 1
    #print("     total = " + str(total))
    #print("     len(sauvegarde_requetes) = " + str(len(sauvegarde_requetes)))
    return (total / len(sauvegarde_requetes)) * 100

def logRequetes(sauvegarde_requetes):
    for r in sauvegarde_requetes:
        print(r.toString())

def avg(list):
    res = 0
    for v in list:
        res += v
    return res / len(list)

if __name__ == "__main__":
    question1 = True
    question2 = True
    question3 = True
    question4 = True

    pertefile = "resultsPerte.csv"
    reponsefile = "resultsTempsReponse.csv"
    question3File = "resultsQuestion3.csv"
    question4File = "resultsQuestion4.csv"
    # Ouverture des fichiers    

    # Question 1
    if question1:
        print("Génération du graphe pour la question 1")
        lambdaValues = [0.5, 0.8, 1, 2, 3]

        saveTempsReponse = io.open(reponsefile, "w")
        saveTempsReponse.write("C,lambda,tempsReponse\n")

        for c in [1,2,3,6]:
            print("Génération pour C = " + str(c))
            for _lambda in lambdaValues:
                listeTempsTraitements = []
                for i in range(0, 10):
                    (_, temps_traitement, _) = main(c, _lambda)
                    listeTempsTraitements.append(temps_traitement)
                    saveTempsReponse.write(str(c) + "," + str(_lambda) + "," + str(temps_traitement) + "\n")
        saveTempsReponse.close()
        dataReponse = pandas.read_csv(reponsefile)
        p1 = sns.relplot(data=dataReponse, x="lambda", y="tempsReponse", hue="C", kind="line")
        
    # Question 2
    if question2:
        print("Génération du graphe pour la question 2")
        lambdaValues = [0.2, 0.3, 0.8, 1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
        ## pour C=6
        #lambdaValues = [0.67, 0.672, 0.674, 0.676, 0.678, 0.679]
        ## pour C=3
        #lambdaValues = [0.762, 0.763, 0.764, 0.765, 0.766, 0.767, 0.768, 0.769]
        ## pour C=2
        #lambdaValues = [0.89, 0.891, 0.892, 0.893, 0.894, 0.895, 0.896, 0.897, 0.898, 0.899, 0.9]
        ## pour C=1
        # lambdaValues = [4.3, 4.34, 4.36, 4.38, 4.4, 4.42, 4.44, 4.46, 4.48, 4.5]

        savePerte = io.open(pertefile, "w")
        savePerte.write("C,lambda,tauxPerte\n")
        for c in [1,2,3,6]:
            print("Génération pour C = " + str(c))
            for _lambda in lambdaValues:
                listePertes = []
                for i in range(0, 30):
                    (tauxPerte, _, _) = main(c, _lambda)
                    listePertes.append(tauxPerte)
                    savePerte.write(str(c) + "," + str(_lambda) + "," + str(tauxPerte) + "\n")
        savePerte.close()
        dataPerte = pandas.read_csv(pertefile)
        p2 = sns.relplot(data=dataPerte, x="lambda", y="tauxPerte", hue="C", kind="line")

    # Question 3
    if question3:
        print("Question 3")
        resultsQuestion3 = io.open(question3File, mode="w")
        resultsQuestion3.write("C,lambda,nbTraitées\n")
        for c in [1, 2, 3, 6]:
            for i in range(0, 30):
                (tauxPerte, tempsReponse, nbTraitees) = main(c, 1)
                resultsQuestion3.write(str(c) + ",1," + str(nbTraitees) + "\n")
        resultsQuestion3.close()
        dataQuestion3 = pandas.read_csv(question3File)
        p3 = sns.relplot(data=dataQuestion3, x="lambda", y="nbTraitées", hue="C")
                
    # Question 4
    if question4:
        print("Question 4")
        resultsQuestion4 = io.open(question4File, mode="w")
        resultsQuestion4.write("C,lambda,nbTraitées\n")
        for c in [1, 2, 3, 6]:
            for _lambda in range (3, 23, 2):
                _lambda /= 10.0
                for i in range(0, 30):
                    (tauxPerte, tempsReponse, nbTraitees) = main(c, _lambda)
                    resultsQuestion4.write(str(c) + "," + str(_lambda) + 
                        "," + str(nbTraitees) + "\n")
        resultsQuestion4.close()
        dataQuestion4 = pandas.read_csv(question4File)
        p4 = sns.relplot(data=dataQuestion4, x="lambda", y="nbTraitées", hue="C", kind="line")

    plt.show()