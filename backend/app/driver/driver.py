from pymongo.mongo_client import MongoClient

class MongoDB:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db = self.client.appdb
    
    def close(self):
        self.client.close()