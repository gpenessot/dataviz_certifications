# Certification Dashboard (en construction)

Ce projet est un tableau de bord interactif pour visualiser et analyser un portfolio de certifications. Il utilise Streamlit pour créer une interface web interactive et Pyvis pour générer un graphe de réseau visualisant les relations entre les certifications.

## Fonctionnalités

- Visualisation graphique des certifications et de leurs relations
- Filtrage des certifications par nom, certification principale et compétences
- Affichage optionnel des compétences dans le graphe
- Analyse des certifications avec des KPI et des graphiques

## Prérequis

- Python 3.10+
- pip

## Installation

1. Clonez ce dépôt :
   ```
   git clone https://github.com/votre-nom-utilisateur/certification-dashboard.git
   cd certification-dashboard
   ```

2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

1. Placez votre fichier de données CSV dans le répertoire `data/` sous le nom `cleaned_data.csv`.

2. Lancez l'application Streamlit :
   ```
   streamlit run src/main.py
   ```

3. Ouvrez votre navigateur et accédez à l'URL indiquée par Streamlit (généralement http://localhost:8501).

## Structure du projet

```
certification-dashboard/
│
├── src/
│   ├── main.py
│   ├── graph.py
│   ├── analysis.py
│   └── utils.py
│
├── data/
│   └── cleaned_data.csv
│
├── cert_radial_tree_graph.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

- `src/main.py` : Point d'entrée de l'application Streamlit
- `src/graph.py` : Contient la classe CertificationGraph pour générer le graphe de réseau
- `src/analysis.py` : Fonctions pour l'analyse et la visualisation des données
- `src/utils.py` : Fonctions utilitaires diverses
- `data/cleaned_data.csv` : Fichier de données des certifications (non inclus dans le repo)

## Contribution

Les contributions à ce projet sont les bienvenues. Veuillez suivre ces étapes pour contribuer :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## Contact

Gaël Penessot - [LinkedIn](https://www.linkedin.com/in/gael-penessot/)

Lien du projet : [https://github.com/gpenessot/dataviz_certifications](https://github.com/gpenessot/dataviz_certifications)

Aperçu du graphe : [Radial Tree](./cert_radial_tree_graph.html)
