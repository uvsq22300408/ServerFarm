# ServerFarm

# Projet Python – Simulation d’une Ferme de Serveurs Spécialisés

## Description du Projet

Ce projet consiste à simuler une ferme de 12 serveurs spécialisés dans le traitement de requêtes. Le but est de déterminer la configuration optimale (valeur de `C`) pour différents taux d’arrivée (`λ`) afin de **minimiser le temps de réponse** et **limiter le taux de perte** des requêtes à **moins de 5%**.

---

## Objectifs

- Simuler le système de serveurs avec différents regroupements `C ∈ {1, 2, 3, 6}`.
- Étudier l’influence de `λ` (paramètre de la loi exponentielle des arrivées).
- Calculer :
  - Le **temps de réponse moyen**.
  - Le **taux de perte** des requêtes.
- Déterminer le **C optimal** pour chaque valeur de `λ` (avec IC 95%).

---

## Modèle à Simuler

- **12 serveurs** regroupés en `C` groupes de `K` serveurs (K = 12 / C).
- **Routeur** :
  - Classe les requêtes et les dirige vers le bon groupe.
  - File FIFO de capacité 100 (perte si pleine).
  - Temps de traitement constant : `T_routeur = (C-1)/C`.
- **Serveurs spécialisés** :
  - Sans file d’attente.
  - Temps de service ~ loi exponentielle, paramètre dépendant de `C` :
    - C = 1 → μ = 4/20
    - C = 2 → μ = 7/20
    - C = 3 → μ = 10/20
    - C = 6 → μ = 14/20
- **Arrivées** :
  - Loi exponentielle de paramètre `λ`.
  - Catégorie tirée uniformément.

---

## Plan de Travail

### 1. Modélisation
- Définir les lois de probabilité utilisées.
- Identifier les événements à simuler (arrivée, traitement routeur, traitement serveur, perte).

### 2. Simulation (par événements discrets)
- Générer les requêtes selon `λ`.
- Gérer la file du routeur.
- Traiter les requêtes via le routeur puis les serveurs spécialisés.
- Collecter les métriques : temps de réponse, pertes, attente.

### 3. Analyse des Résultats
- Courbes :  
  - Temps de réponse moyen (y) vs λ (x), pour chaque `C`.  
  - Taux de perte (y) vs λ (x), pour chaque `C`.
- Ajouter les **intervalles de confiance à 95%**.
- Déterminer les `λ` maximaux pour lesquels perte ≤ 5%.
- Choix optimal de `C` pour un `λ` donné (ex: λ = 1).

---