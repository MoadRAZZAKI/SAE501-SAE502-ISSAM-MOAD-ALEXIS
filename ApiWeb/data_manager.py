import json
from urllib.parse import unquote, quote_plus
from pymongo import MongoClient
import os

class DBConnector:
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('DB_NAME', 'data')
        
        self.uri = unquote(mongo_uri)
        self.db_name = db_name

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

