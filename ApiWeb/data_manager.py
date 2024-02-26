import json
from urllib.parse import unquote, quote_plus
from pymongo import MongoClient

class DBConnector:
    def __init__(self, config_path='C:\\Users\\m.razzaki\\OneDrive - Biodiv-wind\\Bureau\\SAE501\\SAE501\\ApiWeb\\appsettings.json'):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

          
            self.uri = unquote(config['MONGO_URI'])
            self.db_name = config['DB_NAME']

    def connect(self):
        if not self.uri.startswith('mongodb://') and not self.uri.startswith('mongodb+srv://'):
            raise ValueError('Invalid MongoDB URI: %s' % self.uri)

        if '@' in self.uri:
            parts = self.uri.split('@')
            userinfo = parts[0]
            parts[0] = quote_plus(userinfo)
            self.uri = '@'.join(parts)

        client = MongoClient(self.uri, connect=False)
        return client.get_database(self.db_name)