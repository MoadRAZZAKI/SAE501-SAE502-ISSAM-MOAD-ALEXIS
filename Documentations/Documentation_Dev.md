# Documentation pour les développeurs


## 1. Projet: 

Notre logiciel, écrit en Python, offre une solution complète pour surveiller l'attribution, le renouvellement et l'expiration des baux DHCP au sein d'un réseau local. Il est conçu pour fournir une interface utilisateur, une gestion efficace des données via une base de données et une flexibilité grâce à une API REST.

## 2. Fonctionnalités principales :

### a. Interface Graphique :

Notre interface graphique permet de visualiser facilement les informations sur les baux DHCP.
Des fonctionnalités de filtrage et de recherche pour accéder rapidement aux données pertinentes.
Avec notre interface graphique on obtient aussi des alertes visuelles et des notifications pour les événements critiques liés aux baux DHCP.

### b. Base de Données :

Nous avons un stockage sécurisé et efficace des données sur les baux DHCP sur une base de données Mongo-db.

Cette dernière prend en charge de requêtes complexes pour l'analyse.

Avec cette solution de base de données , on assure l'intergrité des données grâce à des mécanismes de sauvegarde et de récupération fournis par l'interface Mongo-DB compass.


### c. API REST :

Nous avons également développer une API RESTful permettant d'interagir avec le système à partir de diverses applications tierces.

Une authentification sécurisée et contrôle d'accès pour garantir la confidentialité des données.


## 2. Partie API WEB (REST) : 

Dans cette partie du projet, j'ai été en charge de la récupération directe des données depuis la base de données Mongo-DB. Ces données sont présentes en temps réel à l'aide du logiciel sniffer.

Comme l'API est un logiciel distinct, j'ai adopté une approche basée sur la Clean Architecture.

J'ai donc structuré le code de l'application en plusieurs couches, chacune ayant une responsabilité spécifique. Ces couches sont organisées comme suit :

- **Couche Domaine** : Cette couche est le fondement de l'architecture. Elle est responsable de la connexion à la base de données.
- **Couche Modules** : Cette couche comprend l'ensemble des fonctions que nous allons utiliser dans notre API.

Étant donné qu'il n'y a pas d'interaction avec l'utilisateur dans ce projet, il n'y a pas de couche d'application, car toutes les données sont présentées au format JSON.






