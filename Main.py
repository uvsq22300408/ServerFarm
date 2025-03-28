from ServerGroup import ServerGroup

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
    tester_groupe_serveurs()
