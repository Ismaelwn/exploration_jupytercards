# JupyterCards - Générateur de Flashcards Interactives

## Contexte et Objectifs 🎯

JupyterCards est un outil conçu pour faciliter l’apprentissage des étudiants en générant automatiquement des flashcards interactives à partir de pages de cours disponibles sur Internet. L'objectif est d'extraire les définitions clés des documents pédagogiques et de les structurer sous forme de cartes d'apprentissage, permettant une révision plus efficace.

## Fonctionnalités 🛠️

- **Extraction automatique des définitions** depuis des documents de cours au format MyST/HTML.
- **Conversion des extraits** en documents HTML exploitables tout en préservant leur représentation originale.
- **Génération de flashcards interactives** pour un apprentissage optimisé.
- **Intégration avec Jupyter Notebooks** pour une meilleure accessibilité aux étudiants.

## Technologies utilisées 🖥️

- **Python** : Extraction et traitement des données.
- **JavaScript** : Interactivité des flashcards.
- **MyST & HTML** : Formats des cours et pages web.
- **JSON (AST - Abstract Syntax Trees)** : Stockage et structuration des définitions.

## Méthodologie 🏗️

1. **Étude des formats** JSON, MyST et HTML pour comprendre leur structure et extraire les définitions pertinentes.
2. **Développement d'un moteur d'extraction** capable de fractionner et d’identifier les définitions à partir des documents sources.
3. **Conversion des définitions en HTML** tout en conservant leur représentation originale.
4. **Intégration des données** sous forme de flashcards interactives utilisables dans un environnement Jupyter.
5. **Tests et validation** en collaboration avec des experts en pédagogie et ingénierie logicielle.

## Collaboration 🤝

Le projet est mené en interaction avec :
- **Un tuteur encadrant**, apportant un suivi technique et méthodologique.
- **Une chercheuse en ingénierie logicielle**, contribuant à l’évaluation des solutions et aux bonnes pratiques de développement.

## Installation 🚀

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Ismaelwn/JupyterCards.git
   ```
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Exécuter l’outil** :
   ```bash
   python main.py
   ```

## Contribuer 📝

Les contributions sont les bienvenues !

1. **Forker le dépôt** 📌
2. **Créer une branche** (`git checkout -b feature/NouvelleFonctionnalite`)
3. **Committer vos modifications** (`git commit -m "Ajout d'une nouvelle méthode d'extraction"`)
4. **Pousser votre branche** (`git push origin feature/NouvelleFonctionnalite`)
5. **Ouvrir une Pull Request** 📬



