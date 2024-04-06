from pymongo.mongo_client import MongoClient

class MongoDB:
    def __init__(self, uri: str, dbname: str):
        self.client = MongoClient(uri)
        self.db = self.client[dbname]
    
    def close(self):
        self.client.close()