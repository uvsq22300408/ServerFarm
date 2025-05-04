# Projet de Simulation – Ferme de serveurs
**Année universitaire : 2024-2025**  
**Auteurs : SOUMET Quentin Theotime TURNEL**

---

## Objectif du projet

Ce projet a pour but de simuler le fonctionnement d'une ferme de 12 serveurs pouvant être regroupés en C catégories spécialisées afin d'optimiser le **temps de réponse** et **réduire les pertes** de requêtes.  
Il s'agit de tester différentes valeurs de **C ∈ {1, 2, 3, 6}**, ainsi que plusieurs **valeurs de λ (taux d'arrivée des requêtes)**, pour observer leur influence sur :
- Le **temps moyen de réponse**.
- Le **taux de perte** (objectif : < 5%).
- Le choix **optimal** de regroupement des serveurs selon les conditions.

---

## Structure du projet

### `eventType.py`
Ce fichier définit les différents **types d’événements** possibles dans la simulation à l’aide d’une énumération (`Enum`) :
- `Arrive` : arrivée d’une nouvelle requête.
- `RouteurDisponible` : le routeur est prêt à traiter une nouvelle requête.
- `RouteurEnvoieSucces` : la requête est transmise avec succès à un serveur.
- `RouteurBloqué` : le routeur est bloqué faute de serveur disponible.

---

### `Event.py`
Définit la classe `Event` représentant un événement dans l’échéancier de la simulation.
- `eventType` : type d’événement.
- `temps` : temps d’occurrence de l’événement.
- `fin` (optionnel) : temps de fin (utile pour le cas de blocage du routeur).

---

### `Requete.py`
Gère la classe `Requete`, qui représente une requête réseau :
- Attributs : temps d’arrivée, catégorie, temps de traitement, état (perdue, terminée).
- Méthodes pour définir les temps de début et fin, marquer une requête comme perdue, etc.

Contient aussi la fonction `nouvelle_requete()` pour générer de nouvelles requêtes à intervalles exponentiels (corrigée selon la loi).

---

### `Routeur.py`
Contient la classe `Routeur`, cœur de la simulation :
- Gère la file d’attente (taille max 100).
- Oriente les requêtes vers les groupes de serveurs spécialisés ou non.
- Traite les requêtes selon un temps fixe dépendant de C.
- Calcule les **événements de blocage**, de succès, et le **taux de perte**.

---

### `Server.py`
Classe `Server`, représentant un serveur individuel :
- Peut être **occupé** ou **libre**.
- Génère un **temps de traitement** selon une loi exponentielle.
- Méthodes pour attribuer une requête, libérer le serveur, etc.

---

### `ServerGroup.py`
Classe `ServerGroup`, représentant un groupe de serveurs (spécialisé ou non) :
- Contient un ensemble de `Server`.
- Gère les taux de service (spécialisé ou non).
- Attribue les requêtes aux serveurs disponibles.

---

## `main.py` – Détail complet de la simulation

Ce fichier orchestre la **simulation événementielle** :
1. **Paramètres initiaux** :
   - `C` : nombre de groupes.
   - `λ` : taux d'arrivée des requêtes.
   - `facteurAccélérationSpécialisé` : accélération des serveurs spécialisés.
   - `limiteTemps` : durée maximale de simulation.

2. **Initialisation** :
   - Création du `Routeur`.
   - Construction des groupes de serveurs avec `ServerGroup`.
   - Définition des spécialités de chaque groupe.
   - Insertion de la première requête dans l’échéancier.

3. **Boucle de simulation** :
   - Tant que le temps n’a pas dépassé `limiteTemps` **et** que le taux de perte est < 5% :
     - Extraction du prochain événement (`echeancier.pop(0)`).
     - Traitement selon le type d’événement :
       - **Arrivée de requête** : tentative d’ajout dans la file du routeur. Si succès, lancement du traitement.
       - **Fin de traitement du routeur** : tentative d’envoi au serveur via le bon groupe. Sinon, le routeur est bloqué.
     - Mise à jour de tous les serveurs.

4. **Statistiques en fin de simulation** :
   - Taux de perte des requêtes.
   - Temps moyen de réponse.
   - Pourcentage de requêtes traitées.

---