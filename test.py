from Routeur import Routeur
from ServerGroup import ServerGroup
from Requete import nouvelle_requete
import time

def test_simulation_simple():
    c = 2  # Nombre de groupes
    nbCategories = c
    nbServeurs = 12
    _lambda = 1
    taux_service = 7 / 20  # pour C = 2
    temps = 0.0

    # === Affichage de la configuration ===
    print("\n=== Configuration de la simulation ===")
    print(f"Nombre total de serveurs      : {nbServeurs}")
    print(f"Nombre de groupes (C)         : {c}")
    print(f"Spécialisation : 1 catégorie par groupe (total {nbCategories})")
    print(f"Serveurs par groupe           : {int(nbServeurs / c)}")
    print(f"Taux de service (µ) pour C={c} : {taux_service:.2f}")
    print("=========================================\n")

    routeur = Routeur(capacite_file=5, nb_categories=nbCategories, c_param=c)

    # Création des groupes spécialisés
    groupes = []
    for i in range(c):
        groupes.append(ServerGroup(i, int(nbServeurs / c), taux_service))

    # Simulation d'un flux de requêtes
    for i in range(10):
        print(f"\n[ÉTAPE {i+1}] Temps : {temps:.2f}")

        # Générer une nouvelle requête
        requete = nouvelle_requete(nbCategories, _lambda, temps)
        print(f"Nouvelle requête : Catégorie {requete.categorie}, Temps arrivée = {requete.temps:.2f}")

        # Mise à jour des serveurs
        for g in groupes:
            g.mettre_a_jour_serveurs(temps)

        # Tentative d’ajout au routeur
        if routeur.ajouter_requete(requete, temps):
            print("Requête ajoutée à la file du routeur.")
        else:
            print("File pleine ! Requête perdue.")

        # Traitement d’une requête si possible
        routeur.traiter(temps, groupes)

        # Avancer le temps artificiellement (pour voir les effets)
        temps += 1.5
        time.sleep(0.3)

    print("\n=== Fin de la simulation test ===")
    print(f"Taux de perte : {routeur.taux_perte() * 100:.2f}%")

if __name__ == "__main__":
    test_simulation_simple()
