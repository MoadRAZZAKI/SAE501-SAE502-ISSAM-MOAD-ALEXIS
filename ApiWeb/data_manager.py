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
