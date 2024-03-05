# Documentation pour les développeurs


## Projet: 

Notre logiciel, écrit en Python, offre une solution complète pour surveiller l'attribution, le renouvellement et l'expiration des baux DHCP au sein d'un réseau local. Il est conçu pour fournir une interface utilisateur, une gestion efficace des données via une base de données et une flexibilité grâce à une API REST.

## Fonctionnalités principales :

### Interface Graphique :

Notre interface graphique permet de visualiser facilement les informations sur les baux DHCP.
Des fonctionnalités de filtrage et de recherche pour accéder rapidement aux données pertinentes.
Avec notre interface graphique on obtient aussi des alertes visuelles et des notifications pour les événements critiques liés aux baux DHCP.

### Base de Données :

Nous avons un stockage sécurisé et efficace des données sur les baux DHCP sur une base de données Mongo-db.

Cette dernière prend en charge de requêtes complexes pour l'analyse.

Avec cette solution de base de données , on assure l'intergrité des données grâce à des mécanismes de sauvegarde et de récupération fournis par l'interface Mongo-DB compass.


### API REST :

Nous avons également développer une API RESTful permettant d'interagir avec le système à partir de diverses applications tierces.

Une authentification sécurisée et contrôle d'accès pour garantir la confidentialité des données.


## 2. Partie API WEB (REST) : 

Dans cette partie du projet, j'ai été en charge de la récupération directe des données depuis la base de données Mongo-DB. Ces données sont présentes en temps réel à l'aide du logiciel sniffer.

Comme l'API est un logiciel distinct, j'ai adopté une approche basée sur la Clean Architecture.

J'ai donc structuré le code de l'application en plusieurs couches, chacune ayant une responsabilité spécifique. Ces couches sont organisées comme suit :

- **Couche Données** : Cette couche est le fondement de l'architecture. Elle est responsable de la connexion à la base de données.
- **Couche Modules** : Cette couche comprend l'ensemble des fonctions que nous allons utiliser dans notre API.

Étant donné qu'il n'y a pas d'interaction avec l'utilisateur dans ce projet, il n'y a pas de couche d'application, car toutes les données sont présentées au format JSON.


## Code (data_manager.py) sous python : 


```python
import json
from urllib.parse import unquote, urlparse, quote_plus
from pymongo import MongoClient

class DBConnector:
    def __init__(self, config_path='C:\\Users\\m.razzaki\\OneDrive - Biodiv-wind\\Bureau\\SAE501\\SAE501\\ApiWeb\\appsettings.json'):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

            self.mongo_username = "root"  # MongoDB user
            self.mongo_password = "password"  # MongoDB mdp

            self.uri = unquote(config['MONGO_URI'])
            self.db_name = config['DB_NAME']

    def connect(self):
        if not self.uri.startswith('mongodb://') and not self.uri.startswith('mongodb+srv://'):
            raise ValueError('Invalid MongoDB URI: %s' % self.uri)

        parsed_uri = urlparse(self.uri)

        # ajout du username et mdp si l'uri ne les contient pas
        if not parsed_uri.username and not parsed_uri.password:
            self.uri = f"mongodb://{quote_plus(self.mongo_username)}:{quote_plus(self.mongo_password)}@{parsed_uri.hostname}:{parsed_uri.port}{parsed_uri.path}"

        # on specifie le type de connexion , avant c'était cnx directe
        client = MongoClient(self.uri)
        return client.get_database(self.db_name)


```



### DBConnector :
La classe `DBConnector` dans notre script Python facilite les connexions à notre base de données MongoDB. Elle nous permet d'interagir avec la collection MongoDB qui stocke les trames DHCP et d'effectuer des opérations sur la base de données. Voici les principaux composants et méthodes :

### Initialisation de la Classe

```python
class DBConnector:
    def __init__(self, config_path='C:\\Users\\m.razzaki\\OneDrive - Biodiv-wind\\Bureau\\SAE501\\SAE501\\ApiWeb\\appsettings.json'):
        """
        Initialise l'instance DBConnector.

        Arguments:
            config_path (str): Chemin vers le fichier de configuration (par défaut : appsettings.json).
        """
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

            # Identifiants MongoDB
            self.mongo_username = "root"
            self.mongo_password = "password"

            # Décodage de l'URI MONGO à partir de la configuration
            self.uri = unquote(config['MONGO_URI'])
            self.db_name = config['DB_NAME']
```

### Connexion à MongoDB

La méthode `connect()` établit une connexion à la base de données MongoDB. Elle gère l'URI, le nom d'utilisateur et le mot de passe. Si l'URI ne commence pas par `mongodb://` ou `mongodb+srv://`, une `ValueError` est levée.

```python
    def connect(self):
        """
        Établit une connexion à la base de données MongoDB.

        En retour:
            pymongo.database.Database : La base de données connectée.
        """
        if not self.uri.startswith('mongodb://') and not self.uri.startswith('mongodb+srv://'):
            raise ValueError(f'URI MongoDB invalide : {self.uri}')

        parsed_uri = urlparse(self.uri)

        # Ajoute le nom d'utilisateur et le mot de passe à l'URI s'ils ne sont pas déjà présents
        if not parsed_uri.username and not parsed_uri.password:
            self.uri = f"mongodb://{quote_plus(self.mongo_username)}:{quote_plus(self.mongo_password)}@{parsed_uri.hostname}:{parsed_uri.port}{parsed_uri.path}"

        # Spécifie le type de connexion (auparavant connexion directe)
        client = MongoClient(self.uri)
        return client.get_database(self.db_name)
```

### Exemple d'utilisation

Pour utiliser le `DBConnector`, il faut créer une instance et appeler la méthode `connect()` :

```python
if __name__ == "__main__":
    connector = DBConnector()
    db = connector.connect()
```

Attention ! il faut remplacer les valeurs fictives (`root`, `password` et le chemin réel du fichier de configuration) par des identifiants MongoDB spécifiques et votre configuration.
