# RogueLike
Projet informatique S2 - update 22/03

Je ferais les commentaires plus tard sur les class-fonctions-méthodes.
A faire : 
- Créer un loop pour les musiques de fond 
- Trier l'inventaire (stacker les items ?)
- Créer des boss
- ...

--- Avant de lancer le jeu ---
Installer pygame : pip install pygame
Télécharger le package sound_manager.rar au lien suivant : 
https://drive.google.com/file/d/1QoRqnRn0m8dKuj2Xk8YpXeL8tOeouQtu/view?usp=sharing
et le décompresser à la racine du dossier.

--- Pour lancer le jeu ---
Un double clic sur engine.py suffira.

--- Figures imposées ---
1 - Factorisation du code : au moins trois modules et noms de classes distincts
        OK largement
2 - Documentation et commentaires du code
        Plus tard
3 - Tests unitaires : (au moins 4 méthodes avec au moins 2 cas testés par méthode)
        Plus tard : Attente réponse du prof
4 - Création d'un type d’objet (classe) : il devra contenir au moins deux  variables d'instance : 
        OK largement

--- 3 Figures parmis les suivantes --- Pour l'instant 2/3 ---
1 - Héritage au moins entre deux types créés
        Pas fait, peut être à envisager
2 - Héritage depuis un type intégré (hors en IHM)
        Ok avec game_states.GameStates et render_functions.RenderOrder qui héritent de enum.Enum
3 - Fonction récursive (dans le cœur du projet)
        Pas eu besoin
4 - Structure de données dynamique (autre que celles intégrées à Python)
        Le dictionnaire en est-il un ? Dans ce cas : OK, sinon à voir
5 - Lecture/ écriture de fichiers : (type de fichier adapté – pas de « pickle »).
        Oui avec le système de sauvegarde, voire le répertoire loader_functions
6 - Accès BDD (serveur BDD à valider avec l’encadrant)
        LOL
7 - Utilisation de calcul vectoriel (évaluer le gain en termes de temps d’exécution).
        Je ne vois pas où
8 - Autres : autres figured peuvent être précisées selon le sujet

Si t'es chaud, implémente d'autres items, monstres et pourquoi pas boss
