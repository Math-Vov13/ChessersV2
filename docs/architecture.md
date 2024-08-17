# Game Architecture

```
ChessersV2/
│
├── main.py                  # Point d'entrée du programme, lance le jeu
├── README.md                # Description du projet, instructions d'installation et d'utilisation
├── requirements.txt         # Liste des dépendances Python (si nécessaire)
├── .gitignore               # Fichiers et dossiers à ignorer par Git
│
├── src/                     # Contient le code source du jeu
│   ├── __init__.py          # Indique que ce dossier est un module Python
│   ├── board.py             # Gestion de l'échiquier (création, mise à jour, affichage)
│   ├── pieces.py            # Définition des pièces (roi, reine, tour, fou, cavalier, pion)
│   ├── game.py              # Logique du jeu (gestion des tours, règles, victoires)
│   ├── player.py            # Gestion des joueurs (humain, IA)
│   ├── move.py              # Gestion des mouvements (vérification des mouvements légaux, historique)
│   ├── ai.py                # Intelligence artificielle (algorithmes de décision pour l'IA)
│   ├── save_manager.py      # Gestion des sauvegardes (enregistrement et chargement des parties)
│   ├── ui/                  # Interface utilisateur
│   │   ├── __init__.py
│   │   ├── console.py       # Interface en ligne de commande
│   │   ├── gui.py           # Interface graphique (ex : avec Pygame ou Tkinter)
│   │   └── assets/          # Fichiers d'assets pour l'interface graphique (images, icônes)
│   │       ├── pieces/      # Images des pièces d'échecs
│   │       └── ...
│   └── utils.py             # Fonctions utilitaires génériques (ex : gestion des entrées/sorties)
│
├── saves/                   # Dossier pour les fichiers de sauvegarde locale
│   └── example_save.json    # Exemple de fichier de sauvegarde (format JSON, par exemple)
│
├── tests/                   # Tests unitaires et d'intégration
│   ├── __init__.py
│   ├── test_board.py        # Tests pour la gestion de l'échiquier
│   ├── test_pieces.py       # Tests pour les pièces
│   ├── test_game.py         # Tests pour la logique du jeu
│   ├── test_move.py         # Tests pour la gestion des mouvements
│   ├── test_ai.py           # Tests pour l'intelligence artificielle
│   ├── test_save_manager.py # Tests pour la gestion des sauvegardes
│   └── ...
│
└── docs/                    # Documentation du projet
    ├── architecture.md      # Description de l'architecture du projet
    ├── api_reference.md     # Référence de l'API interne (si applicable)
    ├── user_manual.md       # Manuel utilisateur (comment jouer)
    └── ...
```