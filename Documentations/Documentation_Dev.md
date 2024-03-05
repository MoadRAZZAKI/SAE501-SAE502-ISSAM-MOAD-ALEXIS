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

Documentation complète de l'API pour faciliter son utilisation par les développeurs tiers.
